"""Mypy type checker command line tool."""

from __future__ import annotations

import mypy.main

import argparse
import os
import subprocess
import sys
import time
from gettext import gettext
from typing import IO, Any, NoReturn, Sequence, TextIO
from typing_extensions import Final

from mypy import build, defaults, state, util
from mypy.config_parser import get_config_module_names, parse_config_file, parse_version
from mypy.errorcodes import error_codes
from mypy.errors import CompileError
from mypy.find_sources import InvalidSourceList, create_source_list
from mypy.fscache import FileSystemCache
from mypy.modulefinder import BuildSource, FindModuleCache, SearchPaths, get_search_dirs, mypy_path
from mypy.options import INCOMPLETE_FEATURES, BuildType, Options
from mypy.split_namespace import SplitNamespace
from mypy.version import __version__

orig_stat: Final = os.stat
MEM_PROFILE: Final = False  # If True, dump memory profile

def main(
    *,
    args: list[str] | None = None,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
    clean_exit: bool = False,
) -> None:
    """Main entry point to the type checker.

    Args:
        args: Custom command-line arguments.  If not given, sys.argv[1:] will
            be used.
        clean_exit: Don't hard kill the process on exit. This allows catching
            SystemExit.
    """
    util.check_python_version("mypy")
    t0 = time.time()
    # To log stat() calls: os.stat = stat_proxy
    sys.setrecursionlimit(2**14)
    if args is None:
        args = sys.argv[1:]

    fscache = FileSystemCache()
    sources, options = mypy.main.process_options(args, stdout=stdout, stderr=stderr, fscache=fscache)
    if clean_exit:
        options.fast_exit = False

    formatter = util.FancyFormatter(stdout, stderr, options.hide_error_codes)

    if options.install_types and (stdout is not sys.stdout or stderr is not sys.stderr):
        # Since --install-types performs user input, we want regular stdout and stderr.
        mypy.main.fail("error: --install-types not supported in this mode of running mypy", stderr, options)

    if options.non_interactive and not options.install_types:
        mypy.main.fail("error: --non-interactive is only supported with --install-types", stderr, options)

    if options.install_types and not options.incremental:
        mypy.main.fail(
            "error: --install-types not supported with incremental mode disabled", stderr, options
        )

    if options.install_types and options.python_executable is None:
        mypy.main.fail(
            "error: --install-types not supported without python executable or site packages",
            stderr,
            options,
        )

    if options.install_types and not sources:
        mypy.main.install_types(formatter, options, non_interactive=options.non_interactive)
        return

    res, messages, blockers = mypy.main.run_build(sources, options, fscache, t0, stdout, stderr)

    if options.non_interactive:
        missing_pkgs = mypy.main.read_types_packages_to_install(options.cache_dir, after_run=True)
        if missing_pkgs:
            # Install missing type packages and rerun build.
            mypy.main.install_types(formatter, options, after_run=True, non_interactive=True)
            fscache.flush()
            print()
            res, messages, blockers = mypy.main.run_build(sources, options, fscache, t0, stdout, stderr)
        mypy.main.show_messages(messages, stderr, formatter, options)

    if MEM_PROFILE:
        from mypy.memprofile import print_memory_profile

        print_memory_profile()

    code = 0
    n_errors, n_notes, n_files = util.count_stats(messages)
    if messages and n_notes < len(messages):
        code = 2 if blockers else 1
    if options.error_summary:
        if n_errors:
            summary = formatter.format_error(
                n_errors, n_files, len(sources), blockers=blockers, use_color=options.color_output
            )
            stdout.write(summary + "\n")
        # Only notes should also output success
        elif not messages or n_notes == len(messages):
            stdout.write(formatter.format_success(len(sources), options.color_output) + "\n")
        stdout.flush()

    if options.install_types and not options.non_interactive:
        result = mypy.main.install_types(formatter, options, after_run=True, non_interactive=False)
        if result:
            print()
            print("note: Run mypy again for up-to-date results with installed types")
            code = 2

    if options.fast_exit:
        # Exit without freeing objects -- it's faster.
        #
        # NOTE: We don't flush all open files on exit (or run other destructors)!
        util.hard_exit(code)
    elif code:
        sys.exit(code)

    # HACK: keep res alive so that mypyc won't free it before the hard_exit
    list([res])

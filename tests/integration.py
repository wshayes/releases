import os
import shutil

from spec import Spec, skip
from invoke import run


class integration(Spec):
    def setup(self):
        self.cwd = os.getcwd()

    def teardown(self):
        os.chdir(self.cwd)

    def _assert_worked(self, folder, opts=None, target='changelog'):
        # Dynamic sphinx opt overrides
        pairs = map(lambda x: '='.join(x), (opts or {}).items())
        flags = map(lambda x: '-D {0}'.format(x), pairs)
        flagstr = ' '.join(flags)
        # Setup
        os.chdir(os.path.join('tests', '_support'))
        build = os.path.join(folder, '_build')
        try:
            # Build
            cmd = 'sphinx-build {2} -c . -W {0} {1}'.format(
                folder, build, flagstr)
            result = run(cmd, warn=True, hide=True)
            # Check for errors
            msg = "Build failed w/ stderr: {0}"
            assert result.ok, msg.format(result.stderr)
            # Check for vaguely correct output
            changelog = os.path.join(build, '{0}.html'.format(target))
            with open(changelog) as fd:
                text = fd.read()
                assert "1.0.1" in text
                assert "#1" in text
        finally:
            shutil.rmtree(build)

    def vanilla_invocation(self):
        # Doctree with just-a-changelog-named-changelog
        self._assert_worked('vanilla')

    def vanilla_with_other_files(self):
        # Same but w/ other files in toctree
        self._assert_worked('vanilla_plus')

    def customized_filename_with_identical_title(self):
        # Changelog named not 'changelog', same title
        self._assert_worked(
            folder='custom_identical',
            opts={'releases_document_name': 'notachangelog'},
            target='notachangelog',
        )

    def customized_filename_with_different_title(self):
        # Changelog named not 'changelog', title distinct
        skip()

    def customized_filename_with_other_files(self):
        # Same as above but w/ other files in toctree
        skip()

    def useful_error_if_changelog_is_missed(self):
        # Don't barf with unknown-node errors if changelog not found.
        skip()
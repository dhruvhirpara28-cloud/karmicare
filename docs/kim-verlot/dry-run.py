"""Kim-only read-only registration check using the existing source-copy runner.
Usage: python3 docs/kim-verlot/dry-run.py SOURCE_COPY_CHECKOUT THEME_ID [SAME_DAY_ATTESTATION]
No write flag is exposed. Template identity and EN hash checks remain in the runner.
"""
import importlib.util
from pathlib import Path
import sys
here = Path(__file__).resolve().parent
runner = Path(sys.argv[1]) / 'docs/localization/registration/register.py'
spec = importlib.util.spec_from_file_location('kim_registration', runner)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
args = ['--lang', 'both', '--theme-id', sys.argv[2]]
if len(sys.argv) > 3:
    args += ['--theme-attested', sys.argv[3]]
# Kim has only template settings: no metaobject, policy or product field bindings.
bindings = str(here / 'template-only-bindings.json')
module.main(args, out=str(here / 'live'), plans=str(here / 'offline-plan-%s.json'),
            bindings_path=bindings, field_bindings_path=bindings,
            shop_objects_path=bindings, shop_policies_path=bindings)

import pytest
from django.core.management import call_command

@pytest.fixture(autouse=True)
def reset_db():
    call_command('flush', '--no-input')
    call_command('migrate')
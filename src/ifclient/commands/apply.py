import click
from ifclient.config.validation.dispatcher import validate_and_resolve
from pydantic import ValidationError
from ifclient.api.client import apply_config
import time

@click.command(name="apply")
@click.argument("config_file", type=click.Path(exists=True, dir_okay=False)) 
@click.option("--skip-empty-files", type=bool, default=False, help="Skip empty files from validation")
def apply_cmd(config_file, skip_empty_files):
    """
    Apply the configuration to the desired projects based on cofiguration
    """
    try:
        # Validate first before applying
        validated_record = validate_and_resolve(config_file, skip_empty_files, is_main=True)
        click.echo(f"Configuration is valid.")

        # Merge the configs based on values
        if getattr(validated_record, 'apiVersion') == "v1":
            from ifclient.config.merger.v1.config_merge import config_merge
            config = config_merge(validated_record)
            for project in config['projects']:
                try:
                    print(f"Updating settings for project: {project['name']}")
                    apply_config(project, config['baseUrl'])
                    print(f"Finished updating settings for project: {project['name']}")
                    time.sleep(3)
                except Exception as e:
                    print(f"{e}")
                    print(f"Could not apply config for project {project['name']}. Skipping it")
                    time.sleep(3)
        else:
            raise ValueError(f"This version is not yet supported")

    except ValidationError as e:
        click.echo(f"Validation error: {e}")
        raise click.ClickException("Validation failed.")
    except Exception as e:
        click.echo(f"Exception: {e}")
        raise click.ClickException("Apply failed.")
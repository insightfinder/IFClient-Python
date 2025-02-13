import click
from ifclient.config.validation.dispatcher import validate_and_resolve
from pydantic import ValidationError
import yaml
import sys

@click.command(name="generate")
@click.argument("config_file", type=click.Path(exists=True, dir_okay=False)) 
@click.option("--skip-empty-files", type=bool, default=False, help="Skip empty files from validation")
@click.argument("output_file", type=click.File("w"), required=False)
def generate_cmd(config_file, skip_empty_files, output_file):
    """
    Generate a json or yaml file as ouput combining all project configurations after resolving 
    """
    try:
        # Validate first before applying
        validated_record = validate_and_resolve(config_file, skip_empty_files, is_main=True)
        click.echo(f"Configuration is valid.")

        # Merge the configs based on values
        if getattr(validated_record, 'apiVersion') == "v1":
            from ifclient.config.merger.v1.config_merge import config_merge
            config = config_merge(validated_record)
            if not output_file:
                stream = sys.stdout
            else:
                stream = output_file
            yaml.dump_all(config['projects'], stream, indent=2)
        else:
            raise ValueError(f"This version is not yet supported")

    except ValidationError as e:
        click.echo(f"Validation error: {e}")
        raise click.ClickException("Validation failed.")
    except Exception as e:
        click.echo(f"Exception: {e}")
        raise click.ClickException("Apply failed.")
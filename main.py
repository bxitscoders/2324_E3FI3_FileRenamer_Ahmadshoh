import click
import os
import re


@click.group()
def cli():
    """
    Command-line tool for batch renaming files in a directory.
    """
    pass


def rename_files(directory, pattern1, pattern2):
    """
    Rename files in the specified directory based on the provided patterns.

    Args:
        directory (str): The directory path where the files are located.
        pattern1 (str): The pattern to search for in file names.
        pattern2 (str): The pattern to replace pattern1 with in file names.
    """
    pattern1_regex = re.compile(re.escape(pattern1).replace(r'\*', r'(.*)'))
    for root, dirs, files in os.walk(directory):
        for file in files:
            match = pattern1_regex.match(file)
            if match:
                wildcard_content = match.group(1) if '*' in pattern1 else ''
                new_file = os.path.join(root, re.sub(pattern1_regex, pattern2.replace('*', wildcard_content), file))
                os.rename(os.path.join(root, file), new_file)
                click.echo(f"Renamed {file} to {os.path.basename(new_file)}")


@click.command()
@click.option(
    '--pattern1',
    prompt='Enter the pattern or filename to search for in file names',
    help='Pattern or filename to search for in file names. Use * as wildcard for any characters.',
)
@click.option(
    '--pattern2',
    prompt='Enter the pattern to replace with in file names',
    help='Pattern to replace pattern1 with in file names. Use * to insert wildcard content from pattern1.',
)
@click.argument('directory', type=click.Path(exists=True), default=os.getcwd())
def rename(directory, pattern1, pattern2):
    """
    Batch rename files in a directory based on the provided patterns.
    """
    click.echo(f"Renaming files in directory: {directory}")
    click.echo(f"Pattern or filename to search for: {pattern1}")
    click.echo(f"Pattern to replace with: {pattern2}")
    rename_files(directory, pattern1, pattern2)
    click.echo("File renaming complete.")


cli.add_command(rename)

if __name__ == '__main__':
    cli()

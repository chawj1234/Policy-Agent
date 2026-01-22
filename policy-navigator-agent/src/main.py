from typing import Optional

import typer

from agent import run

app = typer.Typer(add_completion=False)


@app.command()
def main(
    profile: str = typer.Option(..., "--profile", help="사용자 프로필 문자열"),
    pdf: Optional[str] = typer.Option(None, "--pdf", help="정책 PDF 경로"),
) -> None:
    result = run(profile=profile, pdf_path=pdf)
    print(result)


if __name__ == "__main__":
    app()

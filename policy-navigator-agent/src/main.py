from typing import Optional

import typer

from agent import run

app = typer.Typer(add_completion=False)


@app.command()
def main(
    profile: str = typer.Option(..., "--profile", help="사용자 프로필 문자열"),
    pdf: Optional[str] = typer.Option(None, "--pdf", help="정책 PDF 경로"),
    interactive: bool = typer.Option(False, "--interactive", help="대화형 모드: 질문이 있으면 입력 받고 재평가"),
) -> None:
    result = run(profile=profile, pdf_path=pdf, interactive=interactive)
    print(result)


if __name__ == "__main__":
    app()

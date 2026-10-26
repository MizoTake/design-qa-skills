# Design / QA Skills

[English](README.en.md)

AIコーディングエージェントが、変更をどこに置くかと、何を根拠に品質を判断するかを決めるための2つのSkillです。

- [design](skills/design/SKILL.md): 既存構造を調べ、責務・依存方向・変更範囲・保証する振る舞いを決めます。
- [qa](skills/qa/SKILL.md): 壊れ方と重要リスクから検証を選び、実行した証拠と未検証を分けます。

言語、フレームワーク、特定のエージェント製品に依存しないMarkdownです。それぞれ単独で使えます。Skill本体にPython、Node.js、外部コマンドの実行依存はありません。

## インストール

### 手動

公開リポジトリを取得します。

```sh
git clone https://github.com/MizoTake/design-qa-skills.git
cd design-qa-skills
```

利用するエージェントが認識するSkillディレクトリへ、次のフォルダを丸ごとコピーしてください。同名のSkillがある場合は、上書き前に内容を確認してください。

| コピー元 | コピー先の形 |
| --- | --- |
| `skills/design/` | `利用先のSkillディレクトリ/design/SKILL.md` |
| `skills/qa/` | `利用先のSkillディレクトリ/qa/SKILL.md` |

片方だけでも動作します。コピーするのは各Skillフォルダで、`tests/` や `evals/` は実行時に不要です。Skillの発見方法・自動選択・呼び出し表記は利用先に従います。

### Codex / DeepSeek Harness（DSH）/ OpenCode

3つで共用する場合は、ユーザー共通の `~/.agents/skills/` へ `design/` と `qa/` をコピーします。Windowsの `~` はユーザーフォルダです。各アプリ専用の場所へ重複コピーする必要はありません。

```text
~/.agents/skills/design/SKILL.md
~/.agents/skills/qa/SKILL.md
```

| 利用先 | 呼び出し方 | 読み込み確認 |
| --- | --- | --- |
| Codex | `$design` / `$qa`、または自然言語で指定 | app-serverの `skills/list` で両方が有効、読み込みエラーなし |
| DeepSeek Harness（DSH） | 「designとqaのスキルを使って実装してください」と指定 | インストール済みのSkill Registry / filesystem providerで両方の検出・本文一致 |
| OpenCode | 「designとqaのスキルを使って実装してください」と指定 | 稼働中サービスの `opencode api skill.list` で両方の検出・本文一致 |

2026-10-26、Windows環境でCodex `0.164.0-alpha.11.1`、DSH `0.2.1-rc.3`、OpenCode `2.1.4` を確認しました。これはSkillの検出と読み込みの検証で、モデルへの実装依頼や品質改善効果の測定は含みません。アプリへの導入はコピー方式なので、ソースを更新した場合は導入先も更新し、既存ファイルとの差分を確認してください。

導入後は次のメッセージ、または新しいチャットで指定してください。Codexの共通配置先と `$名前` による呼び出しは[OpenAIの公式ドキュメント](https://learn.chatgpt.com/docs/build-skills)にも記載されています。

### skills CLI（任意）

Node.js / npx がある環境では、作業フォルダから次のコマンドを実行し、CodexやOpenCodeなどの導入先を選べます。事前のcloneは不要です。

```sh
npx skills add MizoTake/design-qa-skills --skill design --skill qa
```

ユーザー全体へ導入する場合は `-g` を付けます。片方だけを導入する場合は、必要な `--skill design` または `--skill qa` だけを指定してください。

```sh
npx skills add MizoTake/design-qa-skills --skill design --skill qa -g
```

DSHを含む3つのアプリで共用する場合は、上記の手動導入で `~/.agents/skills/` に配置できます。skills CLIの利用は任意で、初回にはCLI自体がダウンロードされる場合があります。このCLI経由のインストールは未検証です。

## 使用例

利用先が `$名前` の明示呼び出しをサポートする場合の例です。プロンプトとしてSKILL.mdを渡す環境でも、同じ要求を使えます。

```text
$design 既存の検索機能にキャッシュを追加してください。
既存の責務とキャッシュ境界を確認し、必要最小限の変更にしてください。
```

```text
$qa 保存したHP=0が100に戻る不具合を修正してください。
報告した状態と操作順を再現し、回帰と関連する保存処理を検証してください。
```

```text
$design と $qa を使って、このAPI変更を実装してください。
Designの保証とリスクをQAの検証計画へ引き継いでください。
```

レビュー依頼なら読み取り中心、修正依頼なら許可された変更と検証まで進めます。Skill自体が追加の操作権限を与えることはありません。

## 期待する変化

| 場面 | 避けたい行動 | Skillで求める行動 |
| --- | --- | --- |
| 「キャッシュを追加」 | 既存Serviceへ保存処理を直接足す | 既存境界と責務を調べ、再利用・変更範囲を判断する |
| 「TDDで修正」 | 実装に合わせた期待値やMockだけのテストを書く | 故障の仮説と独立した正解を決め、Redの理由を確認する |
| 「テストが通った」 | 総テスト数だけで完了とする | 関連する回帰・実成果物を確かめ、未検証を明示する |

これは目標とする行動で、改善効果の測定結果ではありません。

## 手順の深さと連携

単純な文言変更では影響確認だけ、小変更では責務と関連検証、中規模以上ではDesign Contract・リスク・Failure Mode・Gateを使います。認証、永続化、公開契約などへの影響が大きければ、行数が少なくても深く確認します。

```text
要求 -> Design -> 保証・不変条件・境界・リスク
                    -> 実装 / QA計画 -> 検証 -> 証拠と未確認事項
```

DesignからQAへ渡す共通項目は `goal`, `contracts`, `invariants`, `boundaries`, `risks`, `compatibility_requirements` です。QA単独の場合は要求と既存コードから必要な保証を抽出します。

設計書・テスト計画書・QA報告書を毎回生成することは求めません。依頼、プロジェクト規約、大きな変更、引き継ぎ、文書自体が成果物となる場合にだけ保存します。特定の設計パターン、Coverage目標、TDD、Unit Testの一律強制も行いません。

## 検証と評価

開発用の検査はPython 3.10以上の標準ライブラリで動きます。追加パッケージはありません。

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -v
```

検査では各Skillのメタデータ、相対リンク、単独コピー、UTF-8、ローカル絶対パス混入、空白・日本語パス、CRLF、任意コマンド不在を扱います。メタデータの検査対象は、この配布物で採用した「`name` とJSON形式で引用した一行の `description`」というYAMLの部分集合です。汎用YAML/Markdownパーサーではなく、外部URLの疎通や見出しアンカーまでは検査しません。

[評価ガイド](evals/README.md)にはDesign・QAの課題、欠陥入りの保存処理、独立した契約テスト、4条件比較の手順があります。意図的な欠陥とMutationを実際に検出できる検証器を用意していますが、Skillを使ったエージェント比較の結果はまだありません。

[CI](.github/workflows/validate.yml)はWindows / macOS / LinuxとPython 3.10 / 3.13を対象にしています。ワークフローの配置は、全OS上での実行成功を意味しません。

## v1の範囲

Skill本体を小さく自己完結させ、配布検査と初期の評価ケースを添えています。Review Skill、製品固有のPlugin Adapter、モデルの自動呼び出し、実利用の失敗を根拠にしていない大量の参照資料は含めません。追加ルールは、実際の失敗を分類し、最小限の修正と対応する評価ケースを組み合わせて育てます。

[変更履歴](CHANGELOG.md)も参照してください。ライセンスは未指定のため、配布ライセンスの宣言はまだ追加していません。

# to4iki/prompt-harness

Work modes for AI coding agents, attached via [rigmode](https://github.com/to4iki/rigmode).

## Setup

```sh
# Point rigmode at this checkout
mkdir -p ~/.config/rigmode
cat > ~/.config/rigmode/config.toml <<EOF
modes_dirs = ["$(pwd)/modes"]
EOF

rigmode hook install claude-code
```

## Modes

- **[implement](./modes/implement.md)** — Change code with a minimal diff, verified by build/test/lint.
- **[pull-request](./modes/pull-request.md)** — Open a pull request described as briefly as it can be.
- **[review](./modes/review.md)** — Review a diff with grounded findings, separating nits from blockers.

#!/usr/bin/env bash
set -euo pipefail

# Ultimate Bug Scanner - Installation Script
# https://github.com/Dicklesworthstone/ultimate_bug_scanner

VERSION="4.4"

# Validate bash version (requires 4.0+)
if ((BASH_VERSINFO[0] < 4)); then
  echo "Error: This installer requires Bash 4.0 or later (you have $BASH_VERSION)" >&2
  echo "Please upgrade bash or install manually." >&2
  exit 1
fi
SCRIPT_NAME="bug-scanner.sh"
INSTALL_NAME="ubs"
REPO_URL="https://raw.githubusercontent.com/Dicklesworthstone/ultimate_bug_scanner/main"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

# Symbols
CHECK="${GREEN}✓${RESET}"
CROSS="${RED}✗${RESET}"
ARROW="${BLUE}→${RESET}"
WARN="${YELLOW}⚠${RESET}"

# Flags
NON_INTERACTIVE=0
SKIP_AST_GREP=0
SKIP_RIPGREP=0
SKIP_HOOKS=0
INSTALL_DIR=""

print_header() {
  echo -e "${BOLD}${BLUE}"
  cat << 'HEADER'
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     ██╗   ██╗██████╗ ███████╗    ██╗███╗   ██╗███████╗████████╗ ║
    ║     ██║   ██║██╔══██╗██╔════╝    ██║████╗  ██║██╔════╝╚══██╔══╝ ║
    ║     ██║   ██║██████╔╝███████╗    ██║██╔██╗ ██║███████╗   ██║    ║
    ║     ██║   ██║██╔══██╗╚════██║    ██║██║╚██╗██║╚════██║   ██║    ║
    ║     ╚██████╔╝██████╔╝███████║    ██║██║ ╚████║███████║   ██║    ║
    ║      ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝    ║
    ║                                                                  ║
HEADER
  echo -e "    ║         ${GREEN}🔬 ULTIMATE BUG SCANNER INSTALLER v${VERSION} 🔬${BLUE}         ║"
  cat << 'HEADER'
    ║                                                                  ║
    ║         Industrial-Grade Static Analysis for JavaScript         ║
    ║              Catch 1000+ Bug Patterns Before Production         ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
HEADER
  echo -e "${RESET}"
}

log() { echo -e "${ARROW} $*"; }
success() { echo -e "${CHECK} $*"; }
error() { echo -e "${CROSS} $*" >&2; }
warn() { echo -e "${WARN} $*"; }

ask() {
  if [ "$NON_INTERACTIVE" -eq 1 ]; then
    return 1  # Default to "no" in non-interactive mode
  fi
  local prompt="$1"
  local response
  read -p "$(echo -e "${YELLOW}?${RESET} ${prompt} (y/N): ")" response
  [[ "$response" =~ ^[Yy]$ ]]
}

can_use_sudo() {
  # Check if sudo is available and can be used without password prompt
  if ! command -v sudo >/dev/null 2>&1; then
    return 1
  fi
  # Check if we can run sudo -n (non-interactive)
  if sudo -n true 2>/dev/null; then
    return 0
  fi
  # If interactive mode, we can potentially use sudo with password
  if [ "$NON_INTERACTIVE" -eq 0 ]; then
    return 0
  fi
  return 1
}

detect_platform() {
  local os
  os="$(uname -s)"
  case "$os" in
    Linux*)   echo "linux" ;;
    Darwin*)  echo "macos" ;;
    CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
    *)        echo "unknown" ;;
  esac
}

detect_shell() {
  if [ -n "${BASH_VERSION:-}" ]; then
    echo "bash"
  elif [ -n "${ZSH_VERSION:-}" ]; then
    echo "zsh"
  else
    # Check default shell
    basename "$SHELL"
  fi
}

get_rc_file() {
  local shell_type
  shell_type="$(detect_shell)"
  case "$shell_type" in
    bash)
      if [ -f "$HOME/.bashrc" ]; then
        echo "$HOME/.bashrc"
      else
        echo "$HOME/.bash_profile"
      fi
      ;;
    zsh)
      echo "$HOME/.zshrc"
      ;;
    *)
      echo "$HOME/.profile"
      ;;
  esac
}

check_ast_grep() {
  if command -v ast-grep >/dev/null 2>&1 || command -v sg >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

install_ast_grep() {
  local platform
  platform="$(detect_platform)"

  log "Installing ast-grep..."

  case "$platform" in
    macos)
      if command -v brew >/dev/null 2>&1; then
        if brew install ast-grep 2>&1 | tee /tmp/ast-grep-install.log; then
          success "ast-grep installed via Homebrew"
          return 0
        else
          error "Homebrew installation failed. Check /tmp/ast-grep-install.log"
          return 1
        fi
      else
        error "Homebrew not found. Please install from: https://ast-grep.github.io/guide/quick-start.html"
        return 1
      fi
      ;;
    linux)
      # Try package managers with proper error handling
      if command -v cargo >/dev/null 2>&1; then
        log "Attempting installation via cargo..."
        if cargo install ast-grep 2>&1 | tee /tmp/ast-grep-install.log; then
          success "ast-grep installed via cargo"
          return 0
        else
          warn "Cargo installation failed, trying npm..."
        fi
      fi

      if command -v npm >/dev/null 2>&1; then
        log "Attempting installation via npm..."
        if npm install -g @ast-grep/cli 2>&1 | tee /tmp/ast-grep-install.log; then
          success "ast-grep installed via npm"
          return 0
        else
          warn "npm installation failed"
        fi
      fi

      warn "All installation methods failed. No package manager available (cargo, npm)"
      log "Download from: https://github.com/ast-grep/ast-grep/releases"
      return 1
      ;;
    windows)
      if command -v cargo >/dev/null 2>&1; then
        if cargo install ast-grep 2>&1 | tee /tmp/ast-grep-install.log; then
          success "ast-grep installed via cargo"
          return 0
        else
          error "Cargo installation failed"
          return 1
        fi
      else
        warn "Install Rust/Cargo or download from: https://ast-grep.github.io/"
        return 1
      fi
      ;;
    *)
      error "Unknown platform. Install manually from: https://ast-grep.github.io/"
      return 1
      ;;
  esac

  # Final verification
  if check_ast_grep; then
    success "ast-grep installed successfully"
    return 0
  else
    error "ast-grep installation failed - command not found after install"
    return 1
  fi
}

check_ripgrep() {
  if command -v rg >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

install_ripgrep() {
  local platform
  platform="$(detect_platform)"

  log "Installing ripgrep..."

  case "$platform" in
    macos)
      if command -v brew >/dev/null 2>&1; then
        if brew install ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
          success "ripgrep installed via Homebrew"
          return 0
        else
          error "Homebrew installation failed. Check /tmp/ripgrep-install.log"
          return 1
        fi
      else
        error "Homebrew not found. Please install from: https://github.com/BurntSushi/ripgrep#installation"
        return 1
      fi
      ;;
    linux)
      # Try package managers with fallback chain
      if command -v cargo >/dev/null 2>&1; then
        log "Attempting installation via cargo..."
        if cargo install ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
          success "ripgrep installed via cargo"
          return 0
        else
          warn "Cargo installation failed, trying system package managers..."
        fi
      fi

      if command -v apt-get >/dev/null 2>&1; then
        if can_use_sudo; then
          log "Attempting installation via apt-get..."
          if timeout 300 sudo apt-get update -qq && timeout 300 sudo apt-get install -y ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
            success "ripgrep installed via apt-get"
            return 0
          else
            warn "apt-get installation failed, trying next method..."
          fi
        else
          warn "sudo not available or not configured, skipping apt-get..."
        fi
      fi

      if command -v dnf >/dev/null 2>&1; then
        if can_use_sudo; then
          log "Attempting installation via dnf..."
          if timeout 300 sudo dnf install -y ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
            success "ripgrep installed via dnf"
            return 0
          else
            warn "dnf installation failed, trying next method..."
          fi
        else
          warn "sudo not available, skipping dnf..."
        fi
      fi

      if command -v pacman >/dev/null 2>&1; then
        if can_use_sudo; then
          log "Attempting installation via pacman..."
          if timeout 300 sudo pacman -S --noconfirm ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
            success "ripgrep installed via pacman"
            return 0
          else
            warn "pacman installation failed, trying next method..."
          fi
        else
          warn "sudo not available, skipping pacman..."
        fi
      fi

      if command -v snap >/dev/null 2>&1; then
        if can_use_sudo; then
          log "Attempting installation via snap..."
          if timeout 300 sudo snap install ripgrep --classic 2>&1 | tee /tmp/ripgrep-install.log; then
            success "ripgrep installed via snap"
            return 0
          else
            warn "snap installation failed"
          fi
        else
          warn "sudo not available, skipping snap..."
        fi
      fi

      warn "All installation methods failed"
      log "Download from: https://github.com/BurntSushi/ripgrep/releases"
      return 1
      ;;
    windows)
      if command -v cargo >/dev/null 2>&1; then
        log "Attempting installation via cargo..."
        if cargo install ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
          success "ripgrep installed via cargo"
          return 0
        else
          warn "Cargo installation failed, trying Windows package managers..."
        fi
      fi

      if command -v scoop >/dev/null 2>&1; then
        log "Attempting installation via scoop..."
        if scoop install ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
          success "ripgrep installed via scoop"
          return 0
        else
          warn "scoop installation failed, trying choco..."
        fi
      fi

      if command -v choco >/dev/null 2>&1; then
        log "Attempting installation via chocolatey..."
        if choco install ripgrep 2>&1 | tee /tmp/ripgrep-install.log; then
          success "ripgrep installed via chocolatey"
          return 0
        else
          warn "chocolatey installation failed"
        fi
      fi

      warn "Install Rust/Cargo, Scoop, or Chocolatey"
      log "Download from: https://github.com/BurntSushi/ripgrep/releases"
      return 1
      ;;
    *)
      error "Unknown platform. Install manually from: https://github.com/BurntSushi/ripgrep#installation"
      return 1
      ;;
  esac

  # Final verification
  if check_ripgrep; then
    success "ripgrep installed successfully"
    return 0
  else
    error "ripgrep installation failed - command not found after install"
    return 1
  fi
}

validate_install_dir() {
  local dir="$1"

  # Security: Prevent installation to dangerous locations
  case "$dir" in
    /|/bin|/sbin|/usr/bin|/usr/sbin|/boot|/dev|/proc|/sys)
      error "Refusing to install to system directory: $dir"
      return 1
      ;;
    /*/../*|*/..|../*|*/../*)
      error "Invalid path (contains ..): $dir"
      return 1
      ;;
    ""|" "*|*" "*)
      error "Invalid path (empty or contains spaces): $dir"
      return 1
      ;;
  esac

  # Must be an absolute path
  if [[ "$dir" != /* ]]; then
    error "Installation directory must be an absolute path: $dir"
    return 1
  fi

  return 0
}

determine_install_dir() {
  if [ -n "$INSTALL_DIR" ]; then
    # Validate user-provided directory
    if ! validate_install_dir "$INSTALL_DIR"; then
      error "Invalid installation directory: $INSTALL_DIR"
      exit 1
    fi
    echo "$INSTALL_DIR"
    return
  fi

  # Prefer ~/.local/bin if it exists or can be created
  if [ -d "$HOME/.local/bin" ] || mkdir -p "$HOME/.local/bin" 2>/dev/null; then
    echo "$HOME/.local/bin"
  elif [ -w "/usr/local/bin" ]; then
    echo "/usr/local/bin"
  else
    echo "$HOME/.local/bin"
  fi
}

install_scanner() {
  local install_dir
  install_dir="$(determine_install_dir)"

  log "Installing Ultimate Bug Scanner to $install_dir..."

  # Create directory if needed
  mkdir -p "$install_dir" 2>/dev/null || {
    error "Cannot create directory: $install_dir"
    return 1
  }

  # Download or copy script
  local script_path="$install_dir/$INSTALL_NAME"
  local temp_path="${script_path}.tmp"

  if [ -f "./$SCRIPT_NAME" ]; then
    # Local installation
    log "Installing from local file..."
    if cp "./$SCRIPT_NAME" "$temp_path" 2>/dev/null; then
      # Verify it's a bash script
      if head -n 1 "$temp_path" | grep -q '^#!/.*bash'; then
        mv "$temp_path" "$script_path"
        success "Copied from local directory"
      else
        error "Local file doesn't appear to be a bash script"
        rm -f "$temp_path"
        return 1
      fi
    else
      error "Failed to copy local file"
      return 1
    fi
  else
    # Remote installation
    log "Downloading from GitHub..."
    local download_url="${REPO_URL}/${SCRIPT_NAME}"

    if command -v curl >/dev/null 2>&1; then
      if curl -fsSL "$download_url" -o "$temp_path" 2>/tmp/download-error.log; then
        log "Downloaded successfully via curl"
      else
        error "Download failed. Check /tmp/download-error.log"
        rm -f "$temp_path"
        return 1
      fi
    elif command -v wget >/dev/null 2>&1; then
      if wget -q "$download_url" -O "$temp_path" 2>/tmp/download-error.log; then
        log "Downloaded successfully via wget"
      else
        error "Download failed. Check /tmp/download-error.log"
        rm -f "$temp_path"
        return 1
      fi
    else
      error "Neither curl nor wget found. Cannot download script."
      return 1
    fi

    # Verify downloaded file
    if [ ! -s "$temp_path" ]; then
      error "Downloaded file is empty"
      rm -f "$temp_path"
      return 1
    fi

    # Check minimum file size (legitimate script should be >10KB)
    local file_size
    file_size=$(wc -c < "$temp_path" 2>/dev/null || echo "0")
    if [ "$file_size" -lt 10240 ]; then
      error "Downloaded file too small ($file_size bytes) - likely incomplete"
      rm -f "$temp_path"
      return 1
    fi

    # Verify shebang (allow for UTF-8 BOM or whitespace)
    local first_line
    first_line=$(head -n 1 "$temp_path" | tr -d '\r\n\t ' | head -c 50)
    if [[ ! "$first_line" =~ ^(\xEF\xBB\xBF)?#!.*bash ]]; then
      error "Downloaded file doesn't appear to be a bash script"
      log "First line: $(head -n 1 "$temp_path" | cat -v)"
      rm -f "$temp_path"
      return 1
    fi

    # Verify critical content markers
    if ! grep -q "ULTIMATE BUG SCANNER" "$temp_path"; then
      error "Downloaded file doesn't appear to be the bug scanner script"
      rm -f "$temp_path"
      return 1
    fi

    # Move to final location
    mv "$temp_path" "$script_path"
  fi

  # Make executable
  chmod +x "$script_path" 2>/dev/null || {
    error "Failed to make script executable"
    return 1
  }

  # Final verification
  if [ -x "$script_path" ] && [ -s "$script_path" ]; then
    success "Installed to: $script_path"

    # Verify it can run
    if "$script_path" --help >/dev/null 2>&1 || "$script_path" -h >/dev/null 2>&1; then
      success "Installation verified - script is functional"
      return 0
    else
      warn "Script installed but may not be fully functional"
      return 0
    fi
  else
    error "Installation failed - file not executable or empty"
    return 1
  fi
}

is_in_path() {
  local dir="$1"
  local normalized_dir

  # Normalize path (resolve symlinks, remove trailing slashes)
  if command -v realpath >/dev/null 2>&1; then
    normalized_dir=$(realpath -s "$dir" 2>/dev/null || echo "$dir")
  else
    normalized_dir="${dir%/}"  # Remove trailing slash
  fi

  # Check each PATH entry
  local IFS=':'
  for path_entry in $PATH; do
    local normalized_entry
    if command -v realpath >/dev/null 2>&1; then
      normalized_entry=$(realpath -s "$path_entry" 2>/dev/null || echo "$path_entry")
    else
      normalized_entry="${path_entry%/}"
    fi

    if [ "$normalized_dir" = "$normalized_entry" ]; then
      return 0
    fi
  done

  return 1
}

add_to_path() {
  local install_dir
  install_dir="$(determine_install_dir)"

  # Check if already in PATH (robust checking)
  if is_in_path "$install_dir"; then
    log "Directory already in PATH"
    return 0
  fi

  local rc_file
  rc_file="$(get_rc_file)"

  # Check if rc_file is writable
  if [ ! -w "$rc_file" ] && [ ! -w "$(dirname "$rc_file")" ]; then
    error "Cannot write to $rc_file - check permissions"
    return 1
  fi

  log "Adding $install_dir to PATH in $rc_file..."

  # Check if PATH entry already exists in file (multiple possible formats)
  if grep -qE "(export )?PATH=.*$install_dir" "$rc_file" 2>/dev/null; then
    log "PATH entry already exists in $rc_file"
    return 0
  fi

  # Add PATH export
  {
    echo ""
    echo "# Ultimate Bug Scanner (added $(date +%Y-%m-%d))"
    echo "export PATH=\"\$PATH:$install_dir\""
  } >> "$rc_file"

  success "Added to PATH in $rc_file"
  warn "⚠ IMPORTANT: Restart your shell or run: source $rc_file"
  return 0
}

create_alias() {
  local install_dir
  install_dir="$(determine_install_dir)"
  local script_path="$install_dir/$INSTALL_NAME"

  # Since the binary is named 'ubs' and will be in PATH, an alias isn't strictly needed
  # But we'll create one for backward compatibility and to ensure it works immediately

  local rc_file
  rc_file="$(get_rc_file)"

  log "Configuring 'ubs' command..."

  # Check if ubs command is already available
  if command -v ubs >/dev/null 2>&1; then
    success "'ubs' command is already available"
    return 0
  fi

  # Check if alias already exists with correct target
  if grep -qF "alias ubs=" "$rc_file" 2>/dev/null; then
    log "Alias already exists, verifying..."
    if grep -qF "alias ubs='$script_path'" "$rc_file" 2>/dev/null || \
       grep -qF "alias ubs=\"$script_path\"" "$rc_file" 2>/dev/null; then
      log "Existing alias is correct"
      return 0
    else
      warn "Existing alias points to different location, updating..."
      # Remove old alias (note: macOS requires the .bak extension, Linux doesn't mind)
      sed -i.bak "/alias ubs=/d" "$rc_file" 2>/dev/null && rm -f "${rc_file}.bak" || {
        warn "Could not update existing alias - you may need to manually remove it"
      }
    fi
  fi

  # Add alias pointing to the installed location
  echo "" >> "$rc_file"
  echo "# Ultimate Bug Scanner alias" >> "$rc_file"
  echo "alias ubs='$script_path'" >> "$rc_file"
  success "Created 'ubs' alias pointing to: $script_path"

  log "Restart your shell or run: source $rc_file"
}

setup_claude_code_hook() {
  if [ ! -d ".claude" ]; then
    log "Not in a project with .claude directory. Skipping..."
    return 0
  fi

  log "Setting up Claude Code hook..."

  local hook_dir=".claude/hooks"
  local hook_file="$hook_dir/on-file-write.sh"

  mkdir -p "$hook_dir"

  cat > "$hook_file" << 'HOOK_EOF'
#!/bin/bash
# Ultimate Bug Scanner - Claude Code Hook
# Runs on every file save for JavaScript/TypeScript files

if [[ "$FILE_PATH" =~ \.(js|jsx|ts|tsx|mjs|cjs)$ ]]; then
  echo "🔬 Running bug scanner..."
  if command -v ubs >/dev/null 2>&1; then
    ubs "${PROJECT_DIR}" --ci 2>&1 | head -50
  else
    bug-scanner.sh "${PROJECT_DIR}" --ci 2>&1 | head -50
  fi
fi
HOOK_EOF

  chmod +x "$hook_file"
  success "Claude Code hook created: $hook_file"
}

setup_git_hook() {
  if [ ! -d ".git" ]; then
    log "Not in a git repository. Skipping..."
    return 0
  fi

  log "Setting up git pre-commit hook..."

  local hook_file=".git/hooks/pre-commit"

  # Backup existing hook if present
  if [ -f "$hook_file" ]; then
    cp "$hook_file" "${hook_file}.backup"
    warn "Existing hook backed up to ${hook_file}.backup"
  fi

  cat > "$hook_file" << 'HOOK_EOF'
#!/bin/bash
# Ultimate Bug Scanner - Pre-commit Hook
# Prevents commits with critical issues

echo "🔬 Running bug scanner..."

if command -v ubs >/dev/null 2>&1; then
  SCANNER="ubs"
else
  SCANNER="bug-scanner.sh"
fi

if ! $SCANNER . --fail-on-warning 2>&1 | tee /tmp/bug-scan.txt | tail -30; then
  echo ""
  echo "❌ Bug scanner found issues. Fix them or use: git commit --no-verify"
  exit 1
fi

echo "✓ No critical issues found"
HOOK_EOF

  chmod +x "$hook_file"
  success "Git pre-commit hook created: $hook_file"
  log "To bypass: git commit --no-verify"
}

add_to_agents_md() {
  local agents_file="AGENTS.md"

  if [ ! -f "$agents_file" ]; then
    log "No AGENTS.md found in current directory"
    return 0
  fi

  # Check if file is writable
  if [ ! -w "$agents_file" ]; then
    error "AGENTS.md exists but is not writable - check permissions"
    return 1
  fi

  # Check if already added (look for the specific section header)
  if grep -qF "## Code Quality: Ultimate Bug Scanner" "$agents_file" 2>/dev/null; then
    log "AGENTS.md already contains scanner documentation"
    return 0
  fi

  log "Adding scanner section to AGENTS.md..."

  # Backup original file
  if ! cp "$agents_file" "${agents_file}.backup" 2>/dev/null; then
    warn "Could not create backup of AGENTS.md"
  fi

  cat >> "$agents_file" << 'AGENTS_EOF'

## Code Quality: Ultimate Bug Scanner

### When to Use

Run the bug scanner **before committing** any JavaScript/TypeScript code changes:

```bash
ubs .
```

### Requirements

- Run automatically after implementing features
- Run before marking work as complete
- Fix all CRITICAL issues before committing
- Consider fixing WARNING issues

### Integration

The scanner may be configured to run automatically via:
- Claude Code hooks (runs on file save)
- Git pre-commit hooks (runs before commit)

If hooks are configured, the scanner runs automatically and you don't need to invoke it manually.

### More Information

See the [Ultimate Bug Scanner repository](https://github.com/Dicklesworthstone/ultimate_bug_scanner) for complete documentation.
AGENTS_EOF

  success "Added section to AGENTS.md"
}

main() {
  print_header

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --non-interactive)
        NON_INTERACTIVE=1
        shift
        ;;
      --skip-ast-grep)
        SKIP_AST_GREP=1
        shift
        ;;
      --skip-ripgrep)
        SKIP_RIPGREP=1
        shift
        ;;
      --skip-hooks)
        SKIP_HOOKS=1
        shift
        ;;
      --install-dir)
        INSTALL_DIR="$2"
        shift 2
        ;;
      --setup-git-hook)
        setup_git_hook
        exit 0
        ;;
      --setup-claude-hook)
        setup_claude_code_hook
        exit 0
        ;;
      --help)
        echo "Usage: install.sh [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --non-interactive    Skip all prompts (use defaults)"
        echo "  --skip-ast-grep      Skip ast-grep installation"
        echo "  --skip-ripgrep       Skip ripgrep installation"
        echo "  --skip-hooks         Skip hook setup"
        echo "  --install-dir DIR    Custom installation directory"
        echo "  --setup-git-hook     Only set up git hook (no install)"
        echo "  --setup-claude-hook  Only set up Claude Code hook (no install)"
        echo "  --help               Show this help"
        exit 0
        ;;
      *)
        error "Unknown option: $1"
        exit 1
        ;;
    esac
  done

  log "Detected platform: $(detect_platform)"
  log "Detected shell: $(detect_shell)"
  echo ""

  # Check for ast-grep
  if ! check_ast_grep && [ "$SKIP_AST_GREP" -eq 0 ]; then
    warn "ast-grep not found (recommended for best results)"
    if ask "Install ast-grep now?"; then
      install_ast_grep || warn "Continuing without ast-grep (regex mode only)"
    fi
    echo ""
  else
    success "ast-grep is installed"
    echo ""
  fi

  # Check for ripgrep
  if ! check_ripgrep && [ "$SKIP_RIPGREP" -eq 0 ]; then
    warn "ripgrep not found (required for optimal performance)"
    if ask "Install ripgrep now?"; then
      install_ripgrep || warn "Continuing without ripgrep (may use slower grep fallback)"
    fi
    echo ""
  else
    success "ripgrep is installed"
    echo ""
  fi

  # Install the scanner
  if ! install_scanner; then
    error "Installation failed"
    exit 1
  fi
  echo ""

  # Add to PATH
  add_to_path
  echo ""

  # Create alias
  create_alias
  echo ""

  # Setup hooks
  if [ "$SKIP_HOOKS" -eq 0 ]; then
    if ask "Set up Claude Code hook?"; then
      setup_claude_code_hook
    fi
    echo ""

    if ask "Set up git pre-commit hook?"; then
      setup_git_hook
    fi
    echo ""
  fi

  # Add to AGENTS.md
  if [ -f "AGENTS.md" ]; then
    if ask "Add scanner documentation to AGENTS.md?"; then
      add_to_agents_md
    fi
    echo ""
  fi

  # Final instructions
  echo ""
  echo -e "${BOLD}${GREEN}"
  cat << 'SUCCESS'
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     ✨  INSTALLATION COMPLETE! ✨                                ║
    ║                                                                  ║
    ║         Your code quality just leveled up! 🚀                   ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
SUCCESS
  echo -e "${RESET}"
  echo ""

  # Check if ubs command is immediately available
  local cmd_available=0
  if command -v ubs >/dev/null 2>&1; then
    cmd_available=1
  fi

  if [ "$cmd_available" -eq 1 ]; then
    echo -e "${BOLD}${GREEN}┌─ Ready to Use! ✓${RESET}"
    echo -e "${GREEN}│${RESET}"
    echo -e "${GREEN}└──${RESET} The ${BOLD}ubs${RESET} command is available now!"
    echo ""
    echo -e "${BOLD}${BLUE}┌─ Quick Start${RESET}"
    echo -e "${BLUE}│${RESET}"
    echo -e "${BLUE}├──${RESET} ${BOLD}Run scanner:${RESET}    ${GREEN}ubs .${RESET}"
    echo -e "${BLUE}├──${RESET} ${BOLD}Get help:${RESET}       ${GREEN}ubs --help${RESET}"
    echo -e "${BLUE}└──${RESET} ${BOLD}Verbose mode:${RESET}   ${GREEN}ubs -v .${RESET}"
  else
    echo -e "${BOLD}${YELLOW}┌─ Almost Done! (Reload Required)${RESET}"
    echo -e "${YELLOW}│${RESET}"
    echo -e "${YELLOW}└──${RESET} Run: ${BOLD}${GREEN}source $(get_rc_file)${RESET}"
    echo ""
    echo -e "${BOLD}${BLUE}┌─ Then Try${RESET}"
    echo -e "${BLUE}│${RESET}"
    echo -e "${BLUE}├──${RESET} ${BOLD}Run scanner:${RESET}    ${GREEN}ubs .${RESET}"
    echo -e "${BLUE}├──${RESET} ${BOLD}Get help:${RESET}       ${GREEN}ubs --help${RESET}"
    echo -e "${BLUE}└──${RESET} ${BOLD}Verbose mode:${RESET}   ${GREEN}ubs -v .${RESET}"
  fi

  echo ""
  echo -e "${BOLD}${BLUE}📚 Documentation:${RESET} ${BLUE}https://github.com/Dicklesworthstone/ultimate_bug_scanner${RESET}"
  echo ""
  echo -e "${GREEN}${BOLD}Happy bug hunting! 🐛🔫${RESET}"
  echo ""
}

main "$@"

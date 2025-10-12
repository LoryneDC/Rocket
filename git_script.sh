#!/usr/bin/env bash

# Enhanced style configuration
bold=$(tput bold)
reset=$(tput sgr0)

# Improved Andromeda colors
color_title="\033[1;38;5;111m"    # Sky blue
color_option="\033[1;38;5;141m"   # Soft purple
color_success="\033[1;38;5;150m"  # Mint green
color_error="\033[1;38;5;203m"    # Coral red
color_input="\033[1;38;5;122m"    # Bright cyan
color_branch="\033[1;38;5;183m"   # Light purple

# Function to display the pixelated header
show_header() {
  clear
  echo -e "${color_title}"
  echo -e "╔════════════════════════════════════════════╗"
  echo -e "║${bold}                G I T   H U B               ${reset}${color_title}║"
  echo -e "╚════════════════════════════════════════════╝${reset}"
  echo -e "${reset}"
}

show_header

# Verify Git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo -e "${color_error}✖ Error: You are not inside a Git repository${reset}"
  exit 1
fi

# Get current branch
current_branch=$(git branch --show-current)

# Step 1: Git Add
echo -e "${color_option}⋆ ${bold}Step 1/3:${reset}${color_option} Adding changes (git add)...${reset}"
git add .
add_status=$?

if [ $add_status -ne 0 ]; then
  echo -e "${color_error}✖ Error in git add${reset}"
  exit 1
fi

# Step 2: Git Commit
echo -e "\n${color_option}⋆ ${bold}Step 2/3:${reset}${color_option} Creating commit...${reset}"
echo -e "${color_input}🌱 Commit message:${reset} "
read -p "   " commit_message

if [ -z "$commit_message" ]; then
  commit_message="Checklist update"
fi

git commit -m "$commit_message"
commit_status=$?

# Step 3: Git Push
if [ $commit_status -eq 0 ]; then
  echo -e "\n${color_option}⋆ ${bold}Step 3/3:${reset}${color_option} Pushing changes to ${color_branch}${current_branch}${color_option}...${reset}"
  git push origin $current_branch
  push_status=$?
else
  echo -e "${color_error}✖ Error in git commit${reset}"
  exit 1
fi

# Final result
show_header
if [ $push_status -eq 0 ]; then
  echo -e "${color_success}✔ Changes successfully pushed to GitHub!${reset}"
  echo -e "\n${color_option}↳ Branch:  ${color_branch}${current_branch}"
  echo -e "${color_option}↳ Message: ${reset}\"$commit_message\""
  echo -e "\n${color_success}♪ All changes are now in the cloud ♪${reset}"
else
  echo -e "${color_error}✖ Error in git push${reset}"
  echo -e "\n${color_option}Try manually: ${reset}git push origin ${current_branch}"
fi

echo -e "\n${color_title}Press any key to exit...${reset}"
read -n 1 -s

import subprocess
import time
import os

def commit_changes(i):
    # Step 0: Open (or create) the file and append "a" to it
    try:
        with open("try.txt", "a") as file:
            file.write(i)
        print("Successfully wrote to try.txt")
    except Exception as e:
        print(f"Failed to write to try.txt: {e}")
        return  # Exit if file creation fails

    try:
        # Step 1: Set Git config for rebase on pull
        subprocess.run(["git", "config", "pull.rebase", "true"], check=True)

        # Step 2: Stash any local changes to avoid rebase conflicts
        subprocess.run(["git", "stash"], check=True)

        # Step 3: Fetch and rebase changes from GitHub
        subprocess.run(["git", "fetch", "origin"], check=True)
        subprocess.run(["git", "rebase", "origin/main"], check=True)

        # Step 4: Pop the stashed changes back to the working directory
        subprocess.run(["git", "stash", "pop"], check=True)

        # Step 5: Add all local changes
        subprocess.run(["git", "add", "--all"], check=True)

        # Step 6: Commit local changes
        subprocess.run(["git", "commit", "-m", "讀萬卷書不如寫萬篇文"], check=True)

        # Step 7: Try to push with a retry on conflict
        retry_count = 0
        while retry_count < 3:
            try:
                subprocess.run(["git", "push"], check=True)
                print("Push successful")
                break
            except subprocess.CalledProcessError:
                print("Push conflict, attempting to pull and rebase")
                subprocess.run(["git", "stash"], check=True)
                subprocess.run(["git", "pull", "--rebase"], check=True)
                subprocess.run(["git", "stash", "pop"], check=True)
                retry_count += 1
                time.sleep(2)  # Small delay before retrying
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during git operation: {e}")

# Execute the function
for i in range(30):
    commit_changes(str(i))

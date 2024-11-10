import subprocess
import time

def commit_changes(letter):
    with open("try.txt", "a") as file:
        file.write(letter)
    try:
        # Step 1: Set Git config for rebase on pull
        subprocess.run(["git", "config", "pull.rebase", "true"], check=True)

        # Step 2: Fetch and rebase changes from GitHub
        subprocess.run(["git", "fetch", "origin"], check=True)
        subprocess.run(["git", "rebase", "origin/main"], check=True)

        # Step 3: Add all local changes
        subprocess.run(["git", "add", "--all"], check=True)

        # Step 4: Commit local changes
        subprocess.run(["git", "commit", "-m", "讀萬卷書不如寫萬篇文"], check=True)

        # Step 5: Try to push with a retry on conflict
        retry_count = 0
        while retry_count < 3:
            try:
                subprocess.run(["git", "push"], check=True)
                print("Push successful")
                break
            except subprocess.CalledProcessError:
                print("Push conflict, attempting to pull and rebase")
                subprocess.run(["git", "pull", "--rebase"], check=True)
                retry_count += 1
                time.sleep(2)  # Small delay before retrying
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during git operation: {e}")

for i in range(100):
    commit_change(i)
    time.sleep(10)

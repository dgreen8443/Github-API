 echo %1>target.txt & echo %2>user.txt & echo %3>auth.txt & docker build -t github-access . & docker run -t -v "%cd%"/output:/external github-access 
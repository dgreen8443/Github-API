echo $1>target.txt;
echo $2>user.txt;
echo $3>auth.txt;
docker build -t github-access . ;
docker run -t -v "$(pwd)"/output:/external github-access ;
xdg-open output/commits.png ;
xdg-open output/followers_languages.png ;
xdg-open output/following_languages.png ;

# Source environment variables
source ../config.env

# Check if USERNAME is empty
if [ -z "$USERNAME" ]; then
  echo "username?"
  read USERNAME
fi

# Check if PASSWORD is empty
if [ -z "$PASSWORD" ]; then
  echo "password?"
  read PASSWORD
fi


rclone copy :http:/full-scrolls/Scroll1.volpkg/paths/20230520175435/20230520175435_mask.png ./segments/20230520175435/ --http-url http://$USERNAME:$PASSWORD@dl.ash2txt.org/ --progress --multi-thread-streams=8 --transfers=8
rclone copy :http:/full-scrolls/Scroll1.volpkg/paths/20230520175435/layers/ ./segments/20230520175435/layers/ --http-url http://$USERNAME:$PASSWORD@dl.ash2txt.org/ --progress --multi-thread-streams=8 --transfers=8
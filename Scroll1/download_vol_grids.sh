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

echo "Would you like to download the masked cubes or all the cubes? (masked/all)"
read MASKED
 

# Specify the mask CSV file path
MASK_CSV_FILE="../Volume_Cube_Masks/scroll_1_54_mask.csv"

# Base URL and target directory for rclone
BASE_URL="/full-scrolls/Scroll1.volpkg/volume_grids/20230205180739/"
TARGET_DIR="./volume_grids/20230205180739/"

if [ "$MASKED" == "all" ]; then
  rclone copy ":http:${BASE_URL}" "${TARGET_DIR}" --http-url "http://${USERNAME}:${PASSWORD}@dl.ash2txt.org/" --progress --multi-thread-streams=8 --transfers=8
else

  # Skip the header line of the CSV and read each line
  tail -n +2 "$MASK_CSV_FILE" | while IFS=, read -r jy jx jz; do
    # Format jx, jy, jz with leading zeros to match the volume grid naming convention
    FILENAME=$(printf "cell_yxz_%03d_%03d_%03d.tif" "$jy" "$jx" "$jz")
    
    # Construct the remote and local paths
    REMOTE_PATH="${BASE_URL}${FILENAME}"
    LOCAL_PATH="${TARGET_DIR}"
    
    # Use rclone to download the file
    rclone copy ":http:${REMOTE_PATH}" "${LOCAL_PATH}" --http-url "http://${USERNAME}:${PASSWORD}@dl.ash2txt.org/" --progress --multi-thread-streams=8 --transfers=8
  done
fi

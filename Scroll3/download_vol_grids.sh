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

# Specify the mask CSV file path
MASK_CSV_FILE="../Volume_Cube_Masks/pherc_0332_53.csv"

# Base URL and target directory for rclone
BASE_URL="/full-scrolls/PHerc0332.volpkg/volume_grids/20231027191953/"
TARGET_DIR="./volume_grids/20231027191953/"

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
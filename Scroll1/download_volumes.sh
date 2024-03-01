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

echo "Specify a range of .tifs volumes to download, or all (Ex: [0-1000,3000,4000-5000] or all)"
read RANGE

# Validate input format
if [[ "$RANGE" != "all" ]] && ! [[ "$RANGE" =~ ^(\[[0-9]+(-[0-9]+)?(,[0-9]+(-[0-9]+)?)*\])$ ]]; then
    echo "Unexpected format: $RANGE"
    echo "Please use the format [start-end,start-end,number] or all"
    exit 1
fi

BASE_URL="/full-scrolls/Scroll1.volpkg/volumes/20230205180739/"
TARGET_DIR="./volumes/20230205180739/"

# Function to download files in a specified range or single file
download_range_or_file() {
    if [[ $1 == $2 ]]; then
        # Single file download
        FILENAME=$(printf "%05d.tif" "$1")
        rclone copy ":http:${BASE_URL}${FILENAME}" "${TARGET_DIR}" --http-url "http://${USERNAME}:${PASSWORD}@dl.ash2txt.org/" --progress --multi-thread-streams=8 --transfers=8
    else
        # Range download
        for ((i=$1; i<=$2; i++)); do
            FILENAME=$(printf "%05d.tif" "$i")
            rclone copy ":http:${BASE_URL}${FILENAME}" "${TARGET_DIR}" --http-url "http://${USERNAME}:${PASSWORD}@dl.ash2txt.org/" --progress --multi-thread-streams=8 --transfers=8
        done
    fi
}

# Parse RANGE and download accordingly
if [ "$RANGE" == "all" ]; then
    rclone copy ":http:${BASE_URL}" "${TARGET_DIR}" --http-url "http://${USERNAME}:${PASSWORD}@dl.ash2txt.org/" --progress --multi-thread-streams=8 --transfers=8
else
    # Remove brackets and split the string into ranges or single numbers
    RANGE=$(echo $RANGE | tr -d '[]')
    IFS=',' read -ra ADDR <<< "$RANGE"
    for range in "${ADDR[@]}"; do
        # Check if the range is actually just a single number
        if [[ "$range" =~ ^[0-9]+$ ]]; then
            # Treat single number as both start and end
            download_range_or_file "$range" "$range"
        else
            # Split the range into start and end
            IFS='-' read -ra NUMS <<< "$range"
            download_range_or_file "${NUMS[0]}" "${NUMS[1]}"
        fi
    done
fi

#Default scroll only mask.csv file, (mask the non-scroll cubes)
#change the path here if you want to use a different mask.csv file
#code assumes the yxz coordinates in the .csv are the grids you want to download
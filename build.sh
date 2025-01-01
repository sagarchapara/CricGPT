#!/bin/bash

# Set the paths to the directories containing the Dockerfiles
DOCKERFILE_CLIENT="./client"
DOCKERFILE_SERVER="./server"

# Set output directory for tar files
OUTPUT_DIR="out"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to build for linux/amd64 and convert to tar
process_image() {
  local dockerfile_dir="$1"
  # Extract image name from the directory path (assuming directory name reflects image name)
  local image_name=$(basename "$dockerfile_dir")
  # Create a new image name for the linux/amd64 version
  local target_image="${image_name}_x86"
  local tar_file="${OUTPUT_DIR}/${target_image}.tar.gz"

  echo "Processing Dockerfile in directory: $dockerfile_dir"

  # 1. Build the image for linux/amd64 architecture using the provided Dockerfile
  echo "Building image for linux/amd64: $target_image"
  docker buildx build \
    --platform linux/amd64 \
    -t "$target_image" \
    --load \
    "$dockerfile_dir"

  # Check for build errors
  if [ $? -ne 0 ]; then
    echo "Error building image: $target_image"
    return 1
  fi

  # 2. Export the image to a tar file
  echo "Exporting image to tar file: $tar_file"
  docker save "$target_image" | gzip > "$tar_file"

  # Check for export errors
  if [ $? -ne 0 ]; then
    echo "Error exporting image to tar file: $tar_file"
    return 1
  fi

  echo "Successfully processed Dockerfile in: $dockerfile_dir"
  return 0
}

# Process each Dockerfile directory
process_image "$DOCKERFILE_CLIENT"
process_image "$DOCKERFILE_SERVER"

echo "Finished processing images."

gcloud compute scp --recurse ./out instance-20241209-093618:/home/sagar/cricgpt --zone "asia-south2-b" --project "annular-hexagon-442323-a8"
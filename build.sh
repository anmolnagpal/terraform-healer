#!/bin/bash
set -e

echo "🚀 Building Terraform Auto-Remediation Docker Image..."

# Get version from git tag or use 'latest'
VERSION=${1:-latest}
REGISTRY=${DOCKER_REGISTRY:-your-registry}
IMAGE_NAME="terraform-auto-remediation"
FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}:${VERSION}"

echo "📦 Image: ${FULL_IMAGE}"

# Build image
docker build -t ${FULL_IMAGE} .

# Also tag as latest
if [ "$VERSION" != "latest" ]; then
    docker tag ${FULL_IMAGE} ${REGISTRY}/${IMAGE_NAME}:latest
fi

echo "✅ Build complete!"
echo ""
echo "To push to registry:"
echo "  docker push ${FULL_IMAGE}"
echo ""
echo "To deploy to Kubernetes:"
echo "  kubectl set image deployment/tf-remediation tf-remediation=${FULL_IMAGE} -n terraform-auto-remediation"

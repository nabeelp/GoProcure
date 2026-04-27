# GoProcure

A collection of tools for downloading and organizing GoPro media from its cloud service.

## Tools

- `gopro-download.py`: Download media files from GoPro Cloud
- `gopro-organize.py`: Organize local media files by date and update their metadata to reflect the actual capture date
- `gopro-sync.py`: Download and organize files in one step

## Credentials

To download from GoPro Cloud you need an access token and user ID. The tools accept these via **environment variables** (recommended, and required for Docker) or a **`config.json`** file.

### Option 1 — Environment variables

```bash
export GOPRO_ACCESS_TOKEN=your-token
export GOPRO_USER_ID=your-user-id
```

### Option 2 — config.json

Create a `config.json` file in the project root:

```json
{
  "access_token": "your-token",
  "user_id": "your-user-id"
}
```

A template (`config.json.example`) is included for reference. Environment variables take precedence over `config.json` when both are present.

### How to obtain your credentials

1. Log into the GoPro site
2. Open your browser's Developer Inspector and navigate to the Network tab
3. Set up a filter for `user`
4. Refresh the page or click on a video
5. Once a `user` network request to `api.gopro.com` occurs, click on one and look at the Cookies field
6. Extract the `access_token` and `user_id` cookie values

> **Note:** The access token is temporary (TTL of a few hours), so you may need to repeat this process occasionally.

---

## Running with Docker (recommended)

### Quick start

```bash
# 1. Edit docker-compose.yml and set your credentials
# 2. Build and run
docker compose up
```

Downloaded and organized files are saved to the `./media` folder on your host machine.

### Configuration via docker-compose.yml

All options are controlled through environment variables in `docker-compose.yml`:

| Variable | Default | Description |
|---|---|---|
| `GOPRO_ACCESS_TOKEN` | *(required)* | GoPro API access token |
| `GOPRO_USER_ID` | *(required)* | GoPro user ID |
| `GOPRO_OUTPUT_DIR` | `/data` | Output directory inside the container |
| `GOPRO_INCLUDE_PHOTOS` | `false` | Include photos in download |
| `GOPRO_MAX_ITEMS` | `10000` | Maximum number of items to download |
| `GOPRO_DOWNLOAD_GPMF` | `false` | Download GPMF sidecar data |
| `GOPRO_ORGANIZE_COPY` | `false` | Copy files instead of moving when organizing |
| `GOPRO_RECURSIVE` | `false` | Recursively process subdirectories |
| `GOPRO_DRY_RUN` | `false` | Preview changes without modifying files |
| `GOPRO_VERBOSE` | `false` | Enable verbose logging |

### Running a specific script

Override the default command in `docker-compose.yml`:

```yaml
command: ["python", "gopro-download.py"]   # download only
command: ["python", "gopro-organize.py"]   # organize only
command: ["python", "gopro-sync.py"]       # download + organize (default)
```

Or pass it directly on the command line:

```bash
docker compose run --rm goprocure python gopro-download.py
```

---

## CI/CD — Automated Docker Hub publishing

A GitHub Actions workflow (`.github/workflows/docker-publish.yml`) automatically builds and pushes the Docker image to Docker Hub.

### Trigger behaviour

| Event | Build | Push | Tags applied |
|---|---|---|---|
| Pull request → `main` | Yes | No | *(validation only)* |
| Push to `main` | Yes | Yes | `main`, `latest` |
| Version tag `v1.2.3` | Yes | Yes | `1.2.3`, `1.2`, `latest` |

### One-time setup

Two secrets must be added to the repository before the workflow can push images.

#### 1. Create a Docker Hub access token

1. Log in to [hub.docker.com](https://hub.docker.com)
2. Click your avatar → **Account Settings**
3. Navigate to **Security → Personal access tokens**
4. Click **Generate new token**
5. Give it a description (e.g. `goprocure-github-actions`) and set permissions to **Read & Write**
6. Click **Generate** and copy the token — it is only shown once

#### 2. Add secrets to GitHub

1. Open the repository on GitHub
2. Go to **Settings → Secrets and variables → Actions**
3. Click **New repository secret** for each of the following:

| Secret name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | The access token created above |

Once set, any push to `main` or a version tag will trigger a build and publish the image to `<your-username>/goprocure` on Docker Hub.

### Using the published image

Replace `<your-username>` with your Docker Hub username:

```bash
docker pull <your-username>/goprocure:latest
```

Or update `docker-compose.yml` to use the pre-built image instead of building locally:

```yaml
services:
  goprocure:
    image: <your-username>/goprocure:latest
    environment:
      - GOPRO_ACCESS_TOKEN=your-token
      ...
```

---

## Running locally

### Installation

1. Clone the repository:

```bash
git clone https://github.com/nabeelp/GoProcure.git
cd GoProcure
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set credentials (see [Credentials](#credentials) above), then run:

```bash
python gopro-sync.py --output-dir /path/to/output --include-photos
```

### Download from Cloud

```bash
python gopro-download.py --output-dir DIR [options]
  --include-photos    # Include photos
  --max-items N       # Limit number of items
  --download-gpmf     # Download GPMF sidecar data
  --verbose           # Verbose logging
```

### Organize Local Files

```bash
python gopro-organize.py [DIR] [options]
  --copy              # Copy instead of move
  --recursive         # Process subdirectories
  --dry-run           # Show what would be done without changes
  --verbose           # Verbose logging
```

`DIR` defaults to `GOPRO_OUTPUT_DIR` if the environment variable is set.

### Download and Organize

```bash
python gopro-sync.py --output-dir DIR [options]
  # Supports all options from both tools above
```
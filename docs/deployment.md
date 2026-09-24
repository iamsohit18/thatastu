# Production Deployment

## Deployment Modes

### 1. Docker Compose (Full Stack)
```bash
docker-compose up --build -d
```
Starts:
- PostgreSQL database container on port `5432`
- FastAPI backend on port `8000`
- React operator dashboard on port `3000`

### 2. Standalone Workstation with PREEMPT_RT Linux
1. Configure Linux with low-latency / real-time kernel:
   ```bash
   sudo apt-get install linux-image-rt-amd64
   ```
2. Grant user non-root real-time priorities in `/etc/security/limits.d/99-realtime.conf`:
   ```text
   @robotics - rtprio 98
   @robotics - memlock unlimited
   ```
3. Run backend with `python -m backend.main` and launch Vite frontend.

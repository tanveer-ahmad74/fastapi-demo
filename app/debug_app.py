import uvicorn

import main
# run this for debug

if __name__ == '__main__':
    uvicorn.run(main.app, host='0.0.0.0', port=8000)

# enzyme-visualizer-app

Prerequisites: 
 - Docker Desktop

## Build FastAPI Setup
```bash

1.  Clone the repository and checkout main branch

$ git clone https://github.com/barrancokarenj/enzyme-visualizer-app.git enzyme-visualizer-app

$ checkout branch main

2.  Navigate inside enzyme-visualizer-app/enzyme-visualizer-api folder

$ cd enzyme-visualizer-app/enzyme-visualizer-api

3. Copy contents of .env.example to .env and modify as needed, or use the default for local development

4. Execute the following command

$ docker compose up --build -d


5. Access http://localhost:3001/docs to check if server is running


```

## Build NuxtJS Client Local Setup

```bash

1. Navigate inside enzyme-visualizer-app/enzyme-visualizer-api folder

$ cd enzyme-visualizer-app/enzyme-visualizer-api

2. Install dependencies

$ npm i

3. Copy contents of .env.example to .env, and modify as needed, or use the default for local development


4. Start at localhost:3000

$ npm run dev


5. Access http://localhost:3000


```


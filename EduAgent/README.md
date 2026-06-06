# EduAgent - 个性化学习资源生成与学习多智能体系统

## 项目简介

EduAgent 是一个基于大模型的个性化学习资源生成与学习多智能体系统。系统通过多个专业 AI Agent 协同工作，为学习者提供量身定制的学习路径、资源推荐、学习评估和智能辅导服务。

## 技术栈

### 后端
- **框架**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0
- **数据验证**: Pydantic v2
- **认证**: JWT (python-jose)
- **数据库**: MySQL 8.0
- **缓存**: Redis 7.0
- **AI 框架**: LangGraph
- **大模型**: 讯飞星火 (Spark) / DeepSeek (可通过配置切换)

### 前端
- **框架**: Vue 3.4+ (Composition API)
- **语言**: TypeScript 5.0+
- **状态管理**: Pinia 2.1+
- **UI 组件库**: Element Plus
- **构建工具**: Vite 5.0+
- **HTTP 客户端**: Axios

### 基础设施
- **容器化**: Docker & Docker Compose
- **数据库**: MySQL + Redis

## Agent 模块

| Agent | 功能 | 核心职责 |
|-------|------|---------|
| Profile Agent | 学习者画像生成 | 分析用户背景、目标和偏好，生成个性化学习画像 |
| Path Agent | 学习路径规划 | 根据画像设计阶段化学习路线 |
| Resource Agent | 资源智能生成 | 基于学习路径生成配套学习资源 |
| Evaluate Agent | 学习效果评估 | 评估学习成果，提供反馈建议 |
| Tutor Agent | 智能学习辅导 | 实时答疑，动态调整学习策略 |

## 项目结构

```
EduAgent/
├── backend/                  # 后端应用
│   ├── app/
│   │   ├── api/            # API 路由层
│   │   ├── core/           # 核心配置
│   │   ├── agents/         # AI Agent 实现
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic 模型
│   │   └── services/       # 业务逻辑层
│   └── requirements.txt
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── api/           # API 封装
│   │   ├── components/     # 公共组件
│   │   ├── views/         # 页面视图
│   │   ├── stores/        # Pinia 状态
│   │   ├── router/        # 路由配置
│   │   └── types/         # TypeScript 类型
│   └── package.json
└── docker/                 # Docker 配置
```

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose

### 后端启动

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 配置 .env 中的数据库和 API Key
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### Docker 部署

```bash
docker-compose up -d
```

## API 路由

### 用户认证
- `POST /api/user/register` - 用户注册
- `POST /api/user/login` - 用户登录
- `POST /api/user/logout` - 用户登出
- `GET /api/user/me` - 获取当前用户信息

### Profile Agent
- `POST /api/profile/generate` - 生成学习者画像
- `GET /api/profile/current` - 获取当前画像
- `PUT /api/profile/update` - 更新画像

### Path Agent
- `POST /api/path/generate` - 生成学习路径
- `GET /api/path/current` - 获取当前学习路径
- `PUT /api/path/update` - 更新学习路径

### Resource Agent
- `POST /api/resource/generate` - 生成学习资源
- `GET /api/resource/list` - 获取资源列表
- `GET /api/resource/{id}` - 获取资源详情

### Evaluate Agent
- `POST /api/evaluate/submit` - 提交评估答案
- `GET /api/evaluate/result/{id}` - 获取评估结果
- `GET /api/evaluate/history` - 获取评估历史

### Tutor Agent
- `POST /api/tutor/chat` - 发送聊天消息
- `GET /api/tutor/history` - 获取对话历史

## 开发指南

### 模块独立性
每个 Agent 模块都遵循严格的三层架构：
- `router.py` - 路由定义，仅处理请求转发
- `service.py` - 业务逻辑，独立可测试
- `model.py` - 数据模型定义
- `schema.py` - 请求/响应模型定义

### 测试策略
```bash
# 后端单元测试
pytest backend/tests/unit -v

# 后端集成测试
pytest backend/tests/integration -v

# 前端组件测试
npm run test:unit
```

## 许可证

MIT License

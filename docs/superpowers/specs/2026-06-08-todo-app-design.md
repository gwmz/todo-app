---
name: ""
metadata: 
  node_type: memory
  title: TODO 网站设计文档
  created: 2026-06-08
  status: approved
  originSessionId: 56e97062-ee7a-4488-b7d1-b591aa4c18d9
---

# TODO 网站 — 设计文档

## 概述

一个个人使用的轻量级 TODO 管理网站，注重视觉精致度和使用体验。前后端分离架构，本地直接运行，无需容器化。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + Vite + Composition API + Pinia + Vue Router + TailwindCSS |
| 后端 | Python FastAPI + Uvicorn |
| 数据库 | SQLite (via SQLAlchemy) |
| 部署 | 直接本地运行 |

## 功能模块

### 1. 任务管理 (核心)
- 添加、编辑、删除 TODO 任务
- 标记任务完成/未完成
- 拖拽排序

### 2. 分类系统
- 预置分类：工作、生活、学习、健康、其他
- 自定义分类，支持颜色标记
- 按分类筛选

### 3. 优先级
- 三级：高（红色）、中（橙色）、低（绿色）

### 4. 任务状态
- 待办、进行中、已完成

### 5. 截止日期与提醒
- 设置截止日期
- 任务到期提醒（前端定时轮询）

### 6. 搜索与筛选
- 关键词搜索（标题+备注全文搜索）
- 多条件筛选：分类、状态、优先级、日期范围

### 7. 任务备注
- 支持多行描述的详细内容

## API 设计

### 认证模块
- `POST /api/auth/register` — 注册
- `POST /api/auth/login` — 登录，返回 JWT
- `GET /api/auth/me` — 获取当前用户信息

### 任务模块
- `GET /api/tasks` — 获取任务列表（支持筛选参数）
- `GET /api/tasks/{id}` — 获取单个任务
- `POST /api/tasks` — 创建任务
- `PUT /api/tasks/{id}` — 更新任务
- `DELETE /api/tasks/{id}` — 删除任务
- `PATCH /api/tasks/{id}/status` — 更新任务状态

### 分类模块
- `GET /api/categories` — 获取分类列表
- `POST /api/categories` — 创建分类
- `PUT /api/categories/{id}` — 更新分类
- `DELETE /api/categories/{id}` — 删除分类

## 数据模型

### Task
- `id`: UUID (主键)
- `title`: str (必填, max 200)
- `description`: str (可选)
- `status`: enum (TODO/IN_PROGRESS/DONE)
- `priority`: enum (HIGH/MEDIUM/LOW)
- `due_date`: datetime (可选)
- `reminder_enabled`: bool
- `category_id`: FK → Category
- `created_at`: datetime
- `updated_at`: datetime
- `completed_at`: datetime (可选)
- `user_id`: FK → User

### Category
- `id`: UUID (主键)
- `name`: str
- `color`: str (CSS 颜色)
- `user_id`: FK → User
- `created_at`: datetime

### User
- `id`: UUID (主键)
- `username`: str (唯一)
- `hashed_password`: str
- `email`: str (可选)
- `created_at`: datetime

## UI 设计

### 设计风格
- 精致动效（CSS transition/animation）
- 渐变色彩 + 卡片式设计
- 圆角、阴影、毛玻璃效果
- 响应式布局

### 页面结构
- **首页** — 任务列表，顶部导航栏，分类侧边栏
- **任务详情** — 弹窗或抽屉式编辑
- **设置页** — 分类管理、个人信息

### 图标
- Lucide Icons（轻量、现代）

## 项目结构

```
todo-app/
├── frontend/              # Vue 3 前端
│   ├── src/
│   │   ├── components/    # 可复用组件
│   │   ├── views/         # 页面组件
│   │   ├── composables/   # 组合式函数
│   │   ├── stores/        # Pinia 状态管理
│   │   ├── api/           # API 请求封装
│   │   ├── types/         # TypeScript 类型定义
│   │   └── assets/        # 静态资源
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.ts
├── backend/               # FastAPI 后端
│   ├── app/
│   │   ├── main.py        # 入口
│   │   ├── models.py      # SQLAlchemy 模型
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── crud.py        # 数据库操作
│   │   ├── api/           # 路由
│   │   ├── core/          # 配置、安全
│   │   └── database.py    # 数据库连接
│   ├── requirements.txt
│   └── alembic/           # 数据库迁移
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-06-08-todo-app-design.md
└── README.md
```

## 开发配置

### 前端
- Vue 3 + Vite + TypeScript
- TailwindCSS 用于样式
- Pinia 状态管理
- Vue Router 路由
- Axios HTTP 客户端
- 代理 vite.config.ts → 后端 127.0.0.1:8000

### 后端
- FastAPI + Uvicorn
- SQLAlchemy ORM
- Pydantic v2
- Python-jose 用于 JWT
- Bcrypt 密码加密
- SQLite 数据库文件 `todo.db`

### 启动方式

**后端**：
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**前端**：
```bash
cd frontend
npm install
npm run dev
```

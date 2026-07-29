# TODO Queue Skill — 规格说明

## 概述

基于队列（FIFO）数据模型的 TODO 管理系统。所有操作通过 Python 脚本执行，不直接操作 SQLite 数据库。

## 数据模型

### 存储

- **数据库路径**: `<项目根目录>/.plann/plann.db`
- **数据库类型**: SQLite
- **表名**: `todos`

### todos 表结构

| 列名 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 自增主键 |
| `title` | TEXT | NOT NULL | TODO 标题 |
| `content` | TEXT | | TODO 详细内容 |
| `status` | TEXT | DEFAULT 'REVIEWING' | 状态流转 |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 状态流转

```
REVIEWING  ──[approve]──→  PENDING  ──[next]──→  PROCESSING  ──[finish]──→  DONE
  (未审核)                  (审核通过/待处理)     (处理中)                 (已完成)
```

- `REVIEWING`: 刚 push，待审核
- `PENDING`: 审核通过，等待处理
- `PROCESSING`: 正在处理中
- `DONE`: 处理完成，保留在数据库

每个状态的推进只能通过对应的命令完成，不允许直接修改数据库。

## 命令规范

所有命令通过 Python 脚本 `todo.py` 执行。

```bash
mamba run -n agents python3 /path/to/todo.py <command> [args...]
```

### push — 新增 TODO

```bash
todo.py push "<title>" ["<content>"]
```

- 插入一条 status = `REVIEWING` 的记录
- title 必填，content 可选
- 输出新增记录的 id

**示例:**
```bash
todo.py push "写周报" "本周工作总结"
# Output: Created TODO #1: 写周报 (REVIEWING)
```

### approve — 审核通过

```bash
todo.py approve <id>
```

- 将 id 匹配的记录从 `REVIEWING` → `PENDING`
- 如果 id 不存在，输出错误
- 如果 status 不是 `REVIEWING`，输出错误

**示例:**
```bash
todo.py approve 1
# Output: Approved TODO #1: 写周报 → PENDING
```

### next — 弹出待处理

```bash
todo.py next
```

- 查询最早一条（按 `created_at` 升序）status = `PENDING` 的记录
- 将其 status 更新为 `PROCESSING`
- 输出该记录的 id, title, content
- 如果没有 `PENDING` 的记录，输出提示信息

**示例:**
```bash
todo.py next
# Output: Now processing TODO #1: 写周报
```

### finish — 标记完成

```bash
todo.py finish <id>
```

- 将 id 匹配的记录从 `PROCESSING` → `DONE`
- 如果 id 不存在，输出错误
- 如果 status 不是 `PROCESSING`，输出错误

**示例:**
```bash
todo.py finish 1
# Output: Completed TODO #1: 写周报 → DONE
```

### list — 查看队列（可选增强）

```bash
todo.py list [--status <status>]
```

- 输出当前所有 TODO（按 `created_at` 排序）
- 可选按 status 过滤
- 如果未实现此命令，用户可通过 `sqlite3` 查看（但禁止修改）

## 规则

1. **禁止直接执行 SQL 修改数据** — 所有数据变更必须通过 `todo.py`
2. 禁止跨状态跳转（不可从 `REVIEWING` 直接到 `DONE`）
3. `next` 遵循 FIFO 顺序（按 `created_at` 升序取最早一条）
4. Python 执行必须使用 `mamba run -n agents` 环境
5. `REVIEWING` 状态的 TODO 不得被 `next` 取出

## 错误处理

- 命令参数缺失 → 提示用法
- id 不存在 → 报错 `TODO #<id> not found`
- 状态不匹配 → 报错 `TODO #<id> is in <status>, expected <expected_status>`
- 数据库文件不存在 → 自动创建 `.plann/` 目录和 `plann.db`

## 未来可能扩展

- `list` 命令查看队列
- 队列长度显示
- 支持 content 字段的多行编辑
- 导出/归档已完成 TODO

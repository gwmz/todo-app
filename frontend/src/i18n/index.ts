import { ref, computed } from 'vue'

const defaultLocale = (() => {
  const stored = localStorage.getItem('locale')
  if (stored === 'zh' || stored === 'en') return stored
  return navigator.language.startsWith('zh') ? 'zh' : 'en'
})()

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const messages: Record<string, any> = {
  zh: {
    login: { title: 'TODO', subtitle: 'Sign in to continue', username: '用户名', usernamePlaceholder: '你的用户名', password: '密码', passwordPlaceholder: '••••••••', signIn: '登录', signingIn: '登录中...', noAccount: "还没有账号？", register: '注册', error: '', required: '请填写此字段。' },
    register: { title: 'TODO', subtitle: 'Create your account', username: '用户名', usernamePlaceholder: '你的用户名', password: '密码', passwordPlaceholder: '••••••••', email: '邮箱（可选）', emailPlaceholder: 'you@example.com', register: '注册', registering: '创建中...', haveAccount: '已有账号？', signIn: '登录', error: '', required: '请填写此字段。' },
    main: { title: '我的任务', tasksRemaining: '个待办', settings: '设置', logout: '退出', searchPlaceholder: '搜索任务...', allStatus: '所有状态', toDo: '待办', inProgress: '进行中', done: '已完成', allPriority: '所有优先级', high: '高', medium: '中', low: '低', noTasks: '还没有任务，在上面添加一个吧！' },
    settings: { title: '分类', subtitle: '组织你的任务', placeholder: '分类名称', add: '添加', required: '请填写此字段。' },
    addTask: { titlePlaceholder: '需要做些什么？', descriptionPlaceholder: '描述...', highPriority: '高优先级', mediumPriority: '中优先级', lowPriority: '低优先级', toDo: '待办', inProgress: '进行中', done: '已完成', noCategory: '无分类', advanced: '↑ 高级', details: '↓ 详情', addTask: '添加任务', titleRequired: '请填写此字段。' },
    taskCard: { high: '高', medium: '中', low: '低', due: '截止：' },
  },
  en: {
    login: { title: 'TODO', subtitle: 'Sign in to continue', username: 'Username', usernamePlaceholder: 'your username', password: 'Password', passwordPlaceholder: '••••••••', signIn: 'Sign In', signingIn: 'Signing in...', noAccount: "Don't have an account?", register: 'Register', error: '', required: 'Please fill out this field.' },
    register: { title: 'TODO', subtitle: 'Create your account', username: 'Username', usernamePlaceholder: 'your username', password: 'Password', passwordPlaceholder: '••••••••', email: 'Email (optional)', emailPlaceholder: 'you@example.com', register: 'Register', registering: 'Creating account...', haveAccount: 'Already have an account?', signIn: 'Sign in', error: '', required: 'Please fill out this field.' },
    main: { title: 'My Tasks', tasksRemaining: 'tasks remaining', settings: 'Settings', logout: 'Logout', searchPlaceholder: 'Search tasks...', allStatus: 'All Status', toDo: 'To Do', inProgress: 'In Progress', done: 'Done', allPriority: 'All Priority', high: 'High', medium: 'Medium', low: 'Low', noTasks: 'No tasks yet. Add one above!' },
    settings: { title: 'Categories', subtitle: 'Organize your tasks', placeholder: 'Category name', add: 'Add', required: 'Please fill out this field.' },
    addTask: { titlePlaceholder: 'What needs to be done?', descriptionPlaceholder: 'Description...', highPriority: 'High Priority', mediumPriority: 'Medium Priority', lowPriority: 'Low Priority', toDo: 'To Do', inProgress: 'In Progress', done: 'Done', noCategory: 'No Category', advanced: '↑ Advanced', details: '↓ Details', addTask: 'Add Task', titleRequired: 'Please fill out this field.' },
    taskCard: { high: 'High', medium: 'Medium', low: 'Low', due: 'Due:' },
  },
}

export const locale = ref<'zh' | 'en'>(defaultLocale)

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function translate(key: string, lang: 'zh' | 'en'): string {
  const [ns, ...rest] = key.split('.')
  const namespace = messages[lang]?.[ns]
  if (!namespace) return key
  let val: any = namespace
  for (const k of rest) {
    if (val && typeof val === 'object') val = val[k]
  }
  return val ?? key
}

export function useTranslation() {
  return {
    t: computed(() => (key: string): string => translate(key, locale.value)),
    locale: computed(() => locale.value),
  }
}

export function setLocale(lang: 'zh' | 'en') {
  locale.value = lang
  localStorage.setItem('locale', lang)
}

export function getLocale(): 'zh' | 'en' {
  return locale.value
}

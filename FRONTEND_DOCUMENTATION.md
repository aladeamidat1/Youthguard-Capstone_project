# 🎨 YouthGuard Frontend Documentation

**Complete Frontend Development Guide for YouthGuard Platform**

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack & Architecture](#tech-stack--architecture)
3. [API Integration](#api-integration)
4. [User Interface Design](#user-interface-design)
5. [Component Structure](#component-structure)
6. [Authentication Flow](#authentication-flow)
7. [Page Layouts](#page-layouts)
8. [State Management](#state-management)
9. [Styling Guidelines](#styling-guidelines)
10. [Development Setup](#development-setup)

---

## 🚀 Project Overview

YouthGuard is a multi-role platform serving four distinct user types:
- **Admin**: Platform oversight and approvals
- **Employer**: Job posting and candidate management
- **Facilitator**: Course creation and student management
- **Learner**: Course enrollment, job applications, and micro-task completion

### Core Modules
1. **Authentication & User Management**
2. **Courses System** (Learning)
3. **Jobs System** (Employment)
4. **Earn System** (Micro-tasks)

---

## 🛠️ Tech Stack & Architecture

### Recommended Frontend Stack
```
Frontend Framework: React 18+ with TypeScript
Styling: Tailwind CSS + Headless UI
State Management: Zustand or Redux Toolkit
HTTP Client: Axios
Routing: React Router v6
Forms: React Hook Form + Zod validation
UI Components: Radix UI or Chakra UI
Icons: Lucide React or Heroicons
Charts: Recharts or Chart.js
Date Handling: date-fns
```

### Project Structure
```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── ui/              # Basic UI elements
│   │   ├── forms/           # Form components
│   │   ├── layout/          # Layout components
│   │   └── common/          # Shared components
│   ├── pages/               # Page components
│   │   ├── auth/            # Authentication pages
│   │   ├── dashboard/       # Role-based dashboards
│   │   ├── courses/         # Course-related pages
│   │   ├── jobs/            # Job-related pages
│   │   └── earn/            # Micro-task pages
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API service functions
│   ├── store/               # State management
│   ├── types/               # TypeScript type definitions
│   ├── utils/               # Utility functions
│   ├── constants/           # App constants
│   └── styles/              # Global styles
├── package.json
└── tailwind.config.js
```

---

## 🔌 API Integration

### Base API Configuration
```typescript
// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
    }
    return Promise.reject(error);
  }
);
```

### API Endpoints Reference

#### Authentication Endpoints
```typescript
// src/services/auth.ts
export const authAPI = {
  register: (data: RegisterData) => 
    apiClient.post('/auth/register/', data),
  
  login: (credentials: LoginData) => 
    apiClient.post('/auth/login/', credentials),
  
  refresh: (refreshToken: string) => 
    apiClient.post('/auth/refresh/', { refresh: refreshToken }),
  
  logout: () => 
    apiClient.post('/auth/logout/'),
  
  getProfile: () => 
    apiClient.get('/auth/profile/'),
  
  updateProfile: (data: ProfileData) => 
    apiClient.patch('/auth/profile/', data),
};
```

#### Courses Endpoints
```typescript
// src/services/courses.ts
export const coursesAPI = {
  // Public endpoints
  getCourses: (params?: CourseFilters) => 
    apiClient.get('/courses/', { params }),
  
  getCourse: (id: string) => 
    apiClient.get(`/courses/${id}/`),
  
  // Learner endpoints
  enrollCourse: (courseId: string) => 
    apiClient.post(`/courses/${courseId}/enroll/`),
  
  getMyEnrollments: () => 
    apiClient.get('/courses/my-enrollments/'),
  
  updateProgress: (courseId: string, lessonId: string) => 
    apiClient.post(`/courses/${courseId}/lessons/${lessonId}/complete/`),
  
  // Facilitator endpoints
  createCourse: (data: CourseData) => 
    apiClient.post('/courses/', data),
  
  updateCourse: (id: string, data: CourseData) => 
    apiClient.patch(`/courses/${id}/`, data),
  
  getMyCourses: () => 
    apiClient.get('/courses/my-courses/'),
  
  getStudents: (courseId: string) => 
    apiClient.get(`/courses/${courseId}/students/`),
};
```

#### Jobs Endpoints
```typescript
// src/services/jobs.ts
export const jobsAPI = {
  // Public endpoints
  getJobs: (params?: JobFilters) => 
    apiClient.get('/jobs/', { params }),
  
  getJob: (id: string) => 
    apiClient.get(`/jobs/${id}/`),
  
  // Learner endpoints
  applyJob: (jobId: string, applicationData: ApplicationData) => 
    apiClient.post(`/jobs/${jobId}/apply/`, applicationData),
  
  getMyApplications: () => 
    apiClient.get('/jobs/my-applications/'),
  
  // Employer endpoints
  createJob: (data: JobData) => 
    apiClient.post('/jobs/', data),
  
  updateJob: (id: string, data: JobData) => 
    apiClient.patch(`/jobs/${id}/`, data),
  
  getMyJobs: () => 
    apiClient.get('/jobs/my-jobs/'),
  
  getApplications: (jobId: string) => 
    apiClient.get(`/jobs/${jobId}/applications/`),
  
  updateApplication: (applicationId: string, status: string) => 
    apiClient.patch(`/jobs/applications/${applicationId}/`, { status }),
};
```

#### Earn (Micro-tasks) Endpoints
```typescript
// src/services/earn.ts
export const earnAPI = {
  // Task endpoints
  getTasks: (params?: TaskFilters) => 
    apiClient.get('/tasks/', { params }),
  
  getTask: (id: string) => 
    apiClient.get(`/tasks/${id}/`),
  
  claimTask: (taskId: string) => 
    apiClient.post(`/tasks/${taskId}/claim/`),
  
  submitTask: (taskId: string, submission: TaskSubmission) => 
    apiClient.post(`/tasks/${taskId}/submit/`, submission),
  
  getMyTasks: () => 
    apiClient.get('/tasks/my-tasks/'),
  
  // Wallet endpoints
  getWallet: () => 
    apiClient.get('/wallet/'),
  
  getTransactions: () => 
    apiClient.get('/wallet/transactions/'),
  
  requestWithdrawal: (amount: number, method: string) => 
    apiClient.post('/wallet/withdraw/', { amount, method }),
};
```

---

## 🎨 User Interface Design

### Design System

#### Color Palette
```css
/* Primary Colors */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-600: #2563eb;
--primary-700: #1d4ed8;

/* Success Colors */
--success-50: #f0fdf4;
--success-500: #22c55e;
--success-600: #16a34a;

/* Warning Colors */
--warning-50: #fffbeb;
--warning-500: #f59e0b;
--warning-600: #d97706;

/* Error Colors */
--error-50: #fef2f2;
--error-500: #ef4444;
--error-600: #dc2626;

/* Neutral Colors */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-500: #6b7280;
--gray-900: #111827;
```

#### Typography Scale
```css
/* Font Sizes */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

#### Spacing System
```css
/* Spacing Scale */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

### Component Design Patterns

#### Button Variants
```typescript
// src/components/ui/Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  children,
  onClick,
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
    outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-primary-500',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-primary-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  };
  
  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };
  
  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${
        (disabled || loading) ? 'opacity-50 cursor-not-allowed' : ''
      }`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading && <Spinner className="mr-2" />}
      {children}
    </button>
  );
};
```

---

## 🧩 Component Structure

### Layout Components

#### Main Layout
```typescript
// src/components/layout/MainLayout.tsx
interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { user } = useAuth();
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        {user && <Sidebar />}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
```

#### Header Component
```typescript
// src/components/layout/Header.tsx
const Header: React.FC = () => {
  const { user, logout } = useAuth();
  
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Logo />
            <nav className="hidden md:ml-6 md:flex md:space-x-8">
              <NavLink to="/courses">Courses</NavLink>
              <NavLink to="/jobs">Jobs</NavLink>
              <NavLink to="/earn">Earn</NavLink>
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
            {user ? (
              <UserMenu user={user} onLogout={logout} />
            ) : (
              <div className="space-x-2">
                <Button variant="ghost" as={Link} to="/login">
                  Login
                </Button>
                <Button as={Link} to="/register">
                  Sign Up
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
```

### Form Components

#### Generic Form Wrapper
```typescript
// src/components/forms/FormWrapper.tsx
interface FormWrapperProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent) => void;
  loading?: boolean;
}

const FormWrapper: React.FC<FormWrapperProps> = ({
  title,
  subtitle,
  children,
  onSubmit,
  loading = false,
}) => {
  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">{title}</h2>
        {subtitle && (
          <p className="mt-2 text-sm text-gray-600">{subtitle}</p>
        )}
      </div>
      
      <form onSubmit={onSubmit} className="space-y-4">
        {children}
      </form>
      
      {loading && (
        <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center">
          <Spinner size="lg" />
        </div>
      )}
    </div>
  );
};
```

#### Input Field Component
```typescript
// src/components/forms/InputField.tsx
interface InputFieldProps {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
  required?: boolean;
  error?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const InputField: React.FC<InputFieldProps> = ({
  label,
  name,
  type = 'text',
  placeholder,
  required = false,
  error,
  value,
  onChange,
}) => {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
          error ? 'border-red-300' : 'border-gray-300'
        }`}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};
```

---

## 🔐 Authentication Flow

### Auth Context
```typescript
// src/contexts/AuthContext.tsx
interface AuthContextType {
  user: User | null;
  login: (credentials: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authAPI.getProfile()
        .then(response => setUser(response.data))
        .catch(() => localStorage.removeItem('access_token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);
  
  const login = async (credentials: LoginData) => {
    const response = await authAPI.login(credentials);
    const { access, refresh, user } = response.data;
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    setUser(user);
  };
  
  const register = async (data: RegisterData) => {
    const response = await authAPI.register(data);
    const { access, refresh, user } = response.data;
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    setUser(user);
  };
  
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };
  
  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### Protected Route Component
```typescript
// src/components/ProtectedRoute.tsx
interface ProtectedRouteProps {
  children: React.ReactNode;
  roles?: UserRole[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, roles }) => {
  const { user, loading } = useAuth();
  const location = useLocation();
  
  if (loading) {
    return <LoadingSpinner />;
  }
  
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return <>{children}</>;
};
```

---

## 📱 Page Layouts

### Dashboard Layouts by Role

#### Learner Dashboard
```typescript
// src/pages/dashboard/LearnerDashboard.tsx
const LearnerDashboard: React.FC = () => {
  const { data: stats } = useQuery('learner-stats', () => 
    Promise.all([
      coursesAPI.getMyEnrollments(),
      jobsAPI.getMyApplications(),
      earnAPI.getWallet(),
    ])
  );
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <Button as={Link} to="/earn">
          Start Earning
        </Button>
      </div>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard
          title="Courses Enrolled"
          value={stats?.enrollments?.length || 0}
          icon={BookOpenIcon}
          color="blue"
        />
        <StatsCard
          title="Job Applications"
          value={stats?.applications?.length || 0}
          icon={BriefcaseIcon}
          color="green"
        />
        <StatsCard
          title="Wallet Balance"
          value={`₦${stats?.wallet?.balance || 0}`}
          icon={CurrencyDollarIcon}
          color="purple"
        />
      </div>
      
      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentCourses />
        <RecentTasks />
      </div>
    </div>
  );
};
```

#### Employer Dashboard
```typescript
// src/pages/dashboard/EmployerDashboard.tsx
const EmployerDashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Employer Dashboard</h1>
        <Button as={Link} to="/jobs/create">
          Post New Job
        </Button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatsCard title="Active Jobs" value={12} />
        <StatsCard title="Total Applications" value={156} />
        <StatsCard title="Interviews Scheduled" value={8} />
        <StatsCard title="Hires Made" value={3} />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentJobs />
        <RecentApplications />
      </div>
    </div>
  );
};
```

#### Facilitator Dashboard
```typescript
// src/pages/dashboard/FacilitatorDashboard.tsx
const FacilitatorDashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Facilitator Dashboard</h1>
        <Button as={Link} to="/courses/create">
          Create Course
        </Button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatsCard title="Published Courses" value={5} />
        <StatsCard title="Total Students" value={234} />
        <StatsCard title="Course Completions" value={89} />
        <StatsCard title="Average Rating" value="4.8" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <MyCourses />
        <StudentProgress />
      </div>
    </div>
  );
};
```

### Course Pages

#### Course Listing Page
```typescript
// src/pages/courses/CoursesPage.tsx
const CoursesPage: React.FC = () => {
  const [filters, setFilters] = useState<CourseFilters>({});
  const [searchTerm, setSearchTerm] = useState('');
  
  const { data: courses, isLoading } = useQuery(
    ['courses', filters, searchTerm],
    () => coursesAPI.getCourses({ ...filters, search: searchTerm })
  );
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Courses</h1>
        <SearchInput
          value={searchTerm}
          onChange={setSearchTerm}
          placeholder="Search courses..."
        />
      </div>
      
      <div className="flex gap-6">
        <aside className="w-64 flex-shrink-0">
          <CourseFilters filters={filters} onChange={setFilters} />
        </aside>
        
        <main className="flex-1">
          {isLoading ? (
            <CoursesSkeleton />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses?.map(course => (
                <CourseCard key={course.id} course={course} />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
```

#### Course Detail Page
```typescript
// src/pages/courses/CourseDetailPage.tsx
const CourseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  
  const { data: course, isLoading } = useQuery(
    ['course', id],
    () => coursesAPI.getCourse(id!)
  );
  
  const enrollMutation = useMutation(
    () => coursesAPI.enrollCourse(id!),
    {
      onSuccess: () => {
        // Redirect to course content or show success message
      }
    }
  );
  
  if (isLoading) return <CourseDetailSkeleton />;
  if (!course) return <NotFound />;
  
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <img
          src={course.thumbnail}
          alt={course.title}
          className="w-full h-64 object-cover"
        />
        
        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {course.title}
              </h1>
              <p className="text-gray-600 mb-4">{course.description}</p>
              
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <span>By {course.facilitator.name}</span>
                <span>•</span>
                <span>{course.duration} hours</span>
                <span>•</span>
                <span>{course.students_count} students</span>
              </div>
            </div>
            
            <div className="text-right">
              <div className="text-2xl font-bold text-green-600 mb-2">
                {course.price === 0 ? 'Free' : `₦${course.price}`}
              </div>
              
              {user?.role === 'learner' && (
                <Button
                  onClick={() => enrollMutation.mutate()}
                  loading={enrollMutation.isLoading}
                  disabled={course.is_enrolled}
                >
                  {course.is_enrolled ? 'Enrolled' : 'Enroll Now'}
                </Button>
              )}
            </div>
          </div>
          
          <div className="border-t pt-6">
            <h3 className="text-xl font-semibold mb-4">Course Content</h3>
            <CourseCurriculum lessons={course.lessons} />
          </div>
        </div>
      </div>
    </div>
  );
};
```

---

## 🗂️ State Management

### Zustand Store Example
```typescript
// src/store/useAppStore.ts
interface AppState {
  // UI State
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  
  // User State
  user: User | null;
  
  // Notifications
  notifications: Notification[];
  
  // Actions
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setUser: (user: User | null) => void;
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  // Initial state
  sidebarOpen: true,
  theme: 'light',
  user: null,
  notifications: [],
  
  // Actions
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setTheme: (theme) => set({ theme }),
  setUser: (user) => set({ user }),
  
  addNotification: (notification) => set((state) => ({
    notifications: [
      ...state.notifications,
      { ...notification, id: Date.now().toString() }
    ]
  })),
  
  removeNotification: (id) => set((state) => ({
    notifications: state.notifications.filter(n => n.id !== id)
  })),
}));
```

---

## 🎨 Styling Guidelines

### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        success: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
        },
        error: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

### CSS Custom Properties
```css
/* src/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --radius: 0.5rem;
  }
  
  * {
    @apply border-border;
  }
  
  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}

@layer components {
  .btn {
    @apply inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background;
  }
  
  .btn-primary {
    @apply bg-primary text-primary-foreground hover:bg-primary/90;
  }
  
  .btn-secondary {
    @apply bg-secondary text-secondary-foreground hover:bg-secondary/80;
  }
  
  .card {
    @apply rounded-lg border bg-card text-card-foreground shadow-sm;
  }
}
```

---

## 🚀 Development Setup

### Package.json Dependencies
```json
{
  "name": "youthguard-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0",
    "@tanstack/react-query": "^4.24.0",
    "zustand": "^4.3.0",
    "react-hook-form": "^7.43.0",
    "@hookform/resolvers": "^2.9.0",
    "zod": "^3.20.0",
    "date-fns": "^2.29.0",
    "lucide-react": "^0.312.0",
    "clsx": "^1.2.0",
    "tailwind-merge": "^1.10.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "@vitejs/plugin-react": "^3.1.0",
    "typescript": "^4.9.0",
    "vite": "^4.1.0",
    "tailwindcss": "^3.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "@tailwindcss/forms": "^0.5.0",
    "@tailwindcss/typography": "^0.5.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx",
    "type-check": "tsc --noEmit"
  }
}
```

### Environment Variables
```env
# .env.local
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_APP_NAME=YouthGuard
REACT_APP_VERSION=1.0.0
```

### Vite Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

---

## 📋 Development Checklist

### Phase 1: Foundation
- [ ] Set up React project with TypeScript
- [ ] Configure Tailwind CSS and design system
- [ ] Implement authentication flow
- [ ] Create layout components (Header, Sidebar, Footer)
- [ ] Set up routing with protected routes
- [ ] Implement error boundaries and loading states

### Phase 2: Core Features
- [ ] Build user registration and login forms
- [ ] Create role-based dashboards
- [ ] Implement course listing and detail pages
- [ ] Build job listing and application flow
- [ ] Create micro-task interface
- [ ] Implement wallet and transaction history

### Phase 3: Advanced Features
- [ ] Add real-time notifications
- [ ] Implement file upload functionality
- [ ] Create admin panel for approvals
- [ ] Add search and filtering
- [ ] Implement progress tracking
- [ ] Add responsive mobile design

### Phase 4: Polish
- [ ] Add animations and transitions
- [ ] Implement dark mode
- [ ] Add accessibility features
- [ ] Optimize performance
- [ ] Add comprehensive error handling
- [ ] Implement offline support

---

This documentation provides a complete foundation for building the YouthGuard frontend. Each section can be expanded based on specific requirements and implementation details.
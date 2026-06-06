// User types
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

// Learning Profile types
export interface LearningProfile {
  id: number
  user_id: number
  knowledge_level?: Record<string, string>
  learning_goals?: string[]
  preferred_learning_style?: Record<string, number>
  available_time_per_week?: number
  target_completion_date?: string
  interests?: string[]
  constraints?: Record<string, any>
  raw_analysis?: string
  created_at: string
  updated_at: string
}

export interface ProfileGenerateRequest {
  user_input: string
  existing_profile?: Partial<LearningProfile>
}

// Learning Path types
export interface PathStage {
  id: number
  learning_path_id: number
  stage_order: number
  title: string
  description?: string
  objectives?: string[]
  estimated_hours?: number
  prerequisites?: number[]
  content_summary?: string
  created_at: string
  updated_at: string
}

export interface LearningPath {
  id: number
  user_id: number
  title: string
  description?: string
  target_skill?: string
  total_estimated_hours?: number
  progress: number
  status: 'draft' | 'active' | 'paused' | 'completed'
  raw_plan?: string
  stages: PathStage[]
  created_at: string
  updated_at: string
}

export interface PathGenerateRequest {
  target_skill: string
  current_knowledge: Record<string, string>
  time_available: number
  goals: string[]
  constraints?: Record<string, any>
}

// Resource types
export interface Resource {
  id: number
  creator_id: number
  title: string
  description?: string
  resource_type: 'video' | 'article' | 'exercise' | 'quiz' | 'project'
  content_format: 'markdown' | 'html' | 'video_url' | 'interactive'
  content?: string
  path_stage_id?: number
  tags?: string[]
  difficulty_level?: 'beginner' | 'intermediate' | 'advanced'
  estimated_minutes?: number
  quality_score?: number
  generation_metadata?: Record<string, any>
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface ResourceGenerateRequest {
  path_stage_id: number
  resource_type: 'video' | 'article' | 'exercise' | 'quiz' | 'project'
  topic: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  count?: number
}

// Assessment types
export interface Assessment {
  id: number
  creator_id: number
  title: string
  description?: string
  path_stage_id?: number
  assessment_type: 'quiz' | 'exam' | 'project' | 'self_check'
  questions?: any[]
  max_score?: number
  time_limit_minutes?: number
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface AssessmentResult {
  id: number
  user_id: number
  assessment_id: number
  answers?: Record<string, any>
  score?: number
  percentage?: number
  passed?: boolean
  feedback?: string
  time_spent_seconds?: number
  completed_at?: string
  created_at: string
}

export interface EvaluationRequest {
  assessment_id: number
  answers: Record<string, any>
}

export interface EvaluationResponse {
  result: AssessmentResult
  detailed_feedback: string
  areas_for_improvement: string[]
  strengths: string[]
  recommendations: string[]
}

// Chat types
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  session_id: string
  message: string
  context?: Record<string, any>
}

export interface ChatResponse {
  response: string
  session_id: string
  suggestions: string[]
  conversation_history: ChatMessage[]
}

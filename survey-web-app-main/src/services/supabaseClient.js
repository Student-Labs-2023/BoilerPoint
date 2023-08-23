import { createClient } from '@supabase/supabase-js'

const supabaseUrl = "https://qdsibpkizystoiqpvoxo.supabase.co"
const supabaseAnonKey = ""

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
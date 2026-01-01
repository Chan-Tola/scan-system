<script setup lang="ts">
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import { useAuth } from '@/features/auth/composables/useAuth'

// Using the @ alias instead of ../../../
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const { handleLogin, isLoading, error: apiError } = useAuth()

const schema = yup.object({
  email: yup.string().email('Enter a valid email').required('Required'),
  password: yup.string().min(6, 'Too short').required('Required'),
})

const { handleSubmit, errors, defineField } = useForm({
  validationSchema: schema,
})

const [email, emailProps] = defineField('email')
const [password, passwordProps] = defineField('password')

const onSubmit = handleSubmit((values) => {
  handleLogin(values)
  console.log(values)
})
</script>

<template>
  <div class="animate-in fade-in slide-in-from-bottom-4 duration-700">
    <div class="flex flex-col items-center space-y-4 mb-8">
      <div
        class="flex h-20 w-20 items-center justify-center rounded-full bg-primary shadow-lg ring-4 ring-white dark:ring-slate-900"
      >
        <ShieldCheck class="h-10 w-10 text-primary-foreground" />
      </div>

      <div class="text-center">
        <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-50">
          ScanSystem Pro
        </h1>
        <p class="text-sm font-medium text-muted-foreground">Enterprise Security Dashboard</p>
      </div>
    </div>

    <Card class="border-none shadow-2xl ring-1 ring-slate-200 dark:ring-slate-800">
      <CardHeader class="space-y-1 pb-6 text-center">
        <CardTitle class="text-xl">Login to your account</CardTitle>
        <CardDescription> Enter your email below to login to your account </CardDescription>
      </CardHeader>

      <CardContent>
        <form @submit="onSubmit" class="grid gap-4">
          <div
            v-if="apiError"
            class="p-3 text-sm bg-destructive/10 text-destructive rounded-md font-medium"
          >
            {{ apiError }}
          </div>

          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              v-model="email"
              v-bind="emailProps"
              type="email"
              placeholder="name@example.com"
              :disabled="isLoading"
              class="h-11 bg-slate-50/50"
            />
            <p class="text-xs text-destructive font-medium">{{ errors.email }}</p>
          </div>

          <div class="grid gap-2">
            <div class="flex items-center">
              <Label for="password">Password</Label>
              <a
                href="#"
                class="ml-auto inline-block text-xs text-primary hover:underline underline-offset-4"
              >
                Forgot your password?
              </a>
            </div>
            <Input
              id="password"
              v-model="password"
              v-bind="passwordProps"
              type="password"
              :disabled="isLoading"
              class="h-11 bg-slate-50/50"
            />
            <p class="text-xs text-destructive font-medium">{{ errors.password }}</p>
          </div>

          <Button
            type="submit"
            class="h-11 w-full font-bold transition-transform active:scale-[0.98]"
            :disabled="isLoading"
          >
            <Loader2 v-if="isLoading" class="mr-2 h-4 w-4 animate-spin" />
            <template v-if="isLoading">Signing in...</template>
            <template v-else>Login</template>
          </Button>
        </form>

        <div class="mt-6 text-center text-sm text-muted-foreground">
          Don't have an account?
          <a href="#" class="text-primary hover:underline underline-offset-4 font-semibold"
            >Sign up</a
          >
        </div>
      </CardContent>
    </Card>

    <footer class="mt-8 text-center text-xs text-slate-500">
      &copy; 2025 ScanSystem. All rights reserved.
    </footer>
  </div>
</template>

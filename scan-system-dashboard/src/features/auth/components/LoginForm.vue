<script setup lang="ts">
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import { useAuth } from '../composables/useAuth'

// Using the @ alias instead of ../../../
import { Button } from '../../../components/ui/button'
import { Input } from '../../../components/ui/input'
import { Label } from '../../../components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../../components/ui/card'

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
})
</script>

<template>
  <Card class="border-none shadow-lg md:border md:shadow-sm">
    <CardHeader class="space-y-1">
      <CardTitle class="text-2xl font-bold tracking-tight"> Login to your account </CardTitle>
      <CardDescription> Enter your email below to login to your account </CardDescription>
    </CardHeader>

    <CardContent>
      <form @submit="onSubmit" class="grid gap-4">
        <div v-if="apiError" class="p-3 text-sm bg-destructive/10 text-destructive rounded-md">
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
          />
          <p class="text-xs text-destructive">{{ errors.email }}</p>
        </div>

        <div class="grid gap-2">
          <div class="flex items-center">
            <Label for="password">Password</Label>
            <a href="#" class="ml-auto inline-block text-xs underline underline-offset-4">
              Forgot your password?
            </a>
          </div>
          <Input
            id="password"
            v-model="password"
            v-bind="passwordProps"
            type="password"
            :disabled="isLoading"
          />
          <p class="text-xs text-destructive">{{ errors.password }}</p>
        </div>

        <Button type="submit" class="w-full" :disabled="isLoading">
          <template v-if="isLoading">Signing in...</template>
          <template v-else>Login</template>
        </Button>

        <Button variant="outline" type="button" class="w-full" :disabled="isLoading">
          Login with Google
        </Button>
      </form>

      <div class="mt-4 text-center text-sm">
        Don't have an account?
        <a href="#" class="underline underline-offset-4 font-medium">Sign up</a>
      </div>
    </CardContent>
  </Card>
</template>

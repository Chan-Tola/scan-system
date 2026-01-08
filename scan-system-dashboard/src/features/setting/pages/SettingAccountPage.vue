<script setup lang="ts">
type AccountForm = {
  fullName: string
  email: string
}

const form: AccountForm = {
  fullName: '',
  email: '',
}

const save = async () => {
  // TODO: call API
  // await api.updateProfile(form)
}
</script>

<template>
  <section class="space-y-4">
    <header>
      <h2 class="text-lg font-semibold">Account</h2>
      <p class="text-sm text-muted-foreground">Update your profile information.</p>
    </header>

    <div class="space-y-3">
      <div class="space-y-1">
        <label class="text-sm font-medium">Full name</label>
        <input v-model="form.fullName" class="h-10 w-full rounded-md border bg-background px-3" />
      </div>

      <div class="space-y-1">
        <label class="text-sm font-medium">Email</label>
        <input
          v-model="form.email"
          type="email"
          class="h-10 w-full rounded-md border bg-background px-3"
        />
      </div>

      <div class="flex justify-end">
        <button class="h-10 rounded-md bg-primary px-4 text-primary-foreground" @click="save">
          Save changes
        </button>
      </div>
    </div>
  </section>
</template>

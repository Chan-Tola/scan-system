<script setup lang="ts">
import { ref } from 'vue'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu'
import { Collapsible, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Search, Download, Calendar, MoreVertical, ChevronDown, Plus } from 'lucide-vue-next'

// <CHANGE> Type definitions for user data from JSON response
interface Role {
  id: number
  name: string
  pivot: {
    model_type: string
    model_id: number
    role_id: number
  }
}

interface User {
  id: number
  user_id: number
  office_id: number
  full_name: string
  gender: string
  phone: string
  address: string
  date_of_birth: string
  join_date: string
  shift_start: string
  shift_end: string
  profile_image: string | null
  created_at: string
  updated_at: string
  expanded: boolean
  user: {
    id: number
    username: string
    email: string
    roles: Role[]
  }
  office: {
    id: number
    name: string
  }
}

// <CHANGE> Static data from JSON response
const users = ref<User[]>([
  {
    id: 2,
    user_id: 4,
    office_id: 12,
    full_name: 'Sok Dara Vichea',
    gender: 'male',
    phone: '098776655',
    address: 'Kandal, Cambodia',
    date_of_birth: '1998-12-15',
    join_date: '2024-01-10',
    shift_start: '08:00:00',
    shift_end: '17:00:00',
    profile_image: null,
    created_at: '2026-01-03T05:39:06.000000Z',
    updated_at: '2026-01-03T05:39:06.000000Z',
    expanded: false,
    user: {
      id: 4,
      username: 'dara_vichea',
      email: 'dara.vichea@example.com',
      roles: [
        {
          id: 2,
          name: 'staff',
          pivot: {
            model_type: 'App\\Domain\\v1\\Users\\Models\\User',
            model_id: 4,
            role_id: 2,
          },
        },
      ],
    },
    office: {
      id: 12,
      name: 'Techey',
    },
  },
])

// <CHANGE> Helper function to get user initials
const getInitials = (fullName: string): string => {
  return fullName
    .split(' ')
    .map((name) => name[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// <CHANGE> Helper function to format dates
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

// <CHANGE> Helper function for role badge styling
const getRoleBadgeClass = (role: string | undefined): string => {
  const baseClasses = 'font-medium'
  switch (role?.toLowerCase()) {
    case 'staff':
      return `${baseClasses} bg-blue-100 text-blue-700`
    case 'admin':
      return `${baseClasses} bg-red-100 text-red-700`
    case 'manager':
      return `${baseClasses} bg-purple-100 text-purple-700`
    default:
      return `${baseClasses} bg-gray-100 text-gray-700`
  }
}

// <CHANGE> Create user handler
const handleCreateUser = (): void => {
  console.log('Create User clicked')
  // Add your create user logic here
}
</script>

<template>
  <div class="w-full p-6 bg-gray-50 min-h-screen">
    <!-- Header Section -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="relative">
          <Search class="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
          <Input placeholder="Search name or email..." class="pl-10 w-80" />
        </div>
      </div>

      <div class="flex items-center gap-4">
        <Button variant="outline" class="gap-2">
          <Calendar class="h-4 w-4" />
          Filter Date
        </Button>
        <Button @click="handleCreateUser" class="bg-green-600 hover:bg-green-700 gap-2">
          <Plus class="h-4 w-4" />
          Create User
        </Button>
        <Button class="bg-blue-600 hover:bg-blue-700 gap-2">
          <Download class="h-4 w-4" />
          Export
        </Button>
      </div>
    </div>

    <!-- Table Section -->
    <div class="bg-white rounded-lg shadow">
      <Table>
        <TableHeader>
          <TableRow class="border-b">
            <TableHead class="w-12"></TableHead>
            <TableHead class="font-semibold text-gray-700">USER ID</TableHead>
            <TableHead class="font-semibold text-gray-700">FULL NAME</TableHead>
            <TableHead class="font-semibold text-gray-700">EMAIL</TableHead>
            <TableHead class="font-semibold text-gray-700">PHONE</TableHead>
            <TableHead class="font-semibold text-gray-700">OFFICE</TableHead>
            <TableHead class="font-semibold text-gray-700">ROLE</TableHead>
            <TableHead class="font-semibold text-gray-700">JOIN DATE</TableHead>
            <TableHead class="w-12"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <template v-for="user in users" :key="user.id">
            <!-- Main Row -->
            <TableRow class="border-b hover:bg-gray-50">
              <TableCell>
                <Collapsible v-model:open="user.expanded">
                  <CollapsibleTrigger as-child>
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0">
                      <ChevronDown
                        :class="['h-4 w-4 transition-transform', user.expanded ? 'rotate-180' : '']"
                      />
                    </Button>
                  </CollapsibleTrigger>
                </Collapsible>
              </TableCell>
              <TableCell class="font-semibold text-blue-600"> #{{ user.user_id }} </TableCell>
              <TableCell>
                <div class="flex items-center gap-3">
                  <Avatar class="h-8 w-8">
                    <AvatarImage :src="user.profile_image" />
                    <AvatarFallback>{{ getInitials(user.full_name) }}</AvatarFallback>
                  </Avatar>
                  <span class="text-blue-600 font-medium">{{ user.full_name }}</span>
                </div>
              </TableCell>
              <TableCell class="text-sm text-gray-600">{{ user.user.email }}</TableCell>
              <TableCell class="text-sm">{{ user.phone }}</TableCell>
              <TableCell class="text-sm">{{ user.office.name }}</TableCell>
              <TableCell>
                <Badge :class="getRoleBadgeClass(user.user.roles[0]?.name)">
                  {{ user.user.roles[0]?.name || 'N/A' }}
                </Badge>
              </TableCell>
              <TableCell class="text-sm">{{ formatDate(user.join_date) }}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger as-child>
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0">
                      <MoreVertical class="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>View Details</DropdownMenuItem>
                    <DropdownMenuItem>Edit</DropdownMenuItem>
                    <DropdownMenuItem class="text-red-600">Delete</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>

            <!-- Expandable Details Row -->
            <TableRow v-if="user.expanded" class="bg-gray-50 border-b">
              <TableCell colspan="9">
                <div class="py-4 px-4">
                  <div class="grid grid-cols-2 gap-6 bg-white p-4 rounded border">
                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase">Address</p>
                      <p class="text-sm text-gray-900 mt-1">{{ user.address }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase">Date of Birth</p>
                      <p class="text-sm text-gray-900 mt-1">{{ formatDate(user.date_of_birth) }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase">Shift Start</p>
                      <p class="text-sm text-gray-900 mt-1">{{ user.shift_start }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase">Shift End</p>
                      <p class="text-sm text-gray-900 mt-1">{{ user.shift_end }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase">Gender</p>
                      <p class="text-sm text-gray-900 mt-1 capitalize">{{ user.gender }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase">Created At</p>
                      <p class="text-sm text-gray-900 mt-1">{{ formatDate(user.created_at) }}</p>
                    </div>
                  </div>
                </div>
              </TableCell>
            </TableRow>
          </template>
        </TableBody>
      </Table>
    </div>
  </div>
</template>


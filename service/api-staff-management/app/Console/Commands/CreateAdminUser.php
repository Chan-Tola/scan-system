<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Domain\v1\Users\Models\User;
use Illuminate\Support\Facades\Hash;
use Spatie\Permission\Models\Role;

class CreateAdminUser extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:create-admin-user 
                            {--email=techeyadmin333@gmail.com : Admin email address}
                            {--password=techey333 : Admin password}
                            {--username=admin : Admin username}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create an admin user with admin role';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        config(['auth.defaults.guard' => 'api']);
        $this->info('Creating Admin user...');

        // create admin role
        $adminRole = Role::firstOrCreate(['name'=> 'admin', 'guard_name'=> 'api']);


        if(!$adminRole) {
            $this->error("Failed to create admin role");
        }

        $email = $this->option('email');
        $password = $this->option('password');
        $username = $this->option('username');

        // Check if user already exists
        $existingUser = User::where('email', $email)->first();

        if($existingUser) {
            if(!$this->confirm("User with email '{$email}' already exists. Do you want to update it and assign admin role?",true))
            {
                $this->info("Operation cancelled.");
                return Command::SUCCESS;
            }

            // Update existing user

            $existingUser->update([
                User::USERNAME => $username,
                User::PASSWORD => Hash::make($password),
            ]);

            // Assign admin role ( remove other roles first if needed)
            if(!$existingUser->hasRole('admin', 'api'))
            {
                $existingUser->assignRole($adminRole);
            }

            $this->info('✅ Admin user updated successfully!');
            $this->table(
                ['Field', 'Value'],
                [
                    ['Username', $existingUser->username],
                    ['Email', $existingUser->email],
                    ['Password', $password],
                    ['Role', 'admin'],
                ]
            );
            return Command::SUCCESS;
        }

        // Create new user
        try {
            $user = User::create([
                User::USERNAME => $username,
                User::EMAIL => $email,
                User::PASSWORD => Hash::make($password),
                User::EMAIL_VERIFIED_AT => now(),
            ]);

            // Assign admin role
            $user->assignRole($adminRole);

            $this->info('✅ Admin user created successfully!');
            $this->table(
                ['Field', 'Value'],
                [
                    ['Username', $user->username],
                    ['Email', $user->email],
                    ['Password', $password],
                    ['Role', 'admin'],
                ]
            );

            return Command::SUCCESS;

        } catch (\Exception $e) {
            $this->error('Failed to create admin user: ' . $e->getMessage());
            return Command::FAILURE;
        }
    }
}

# Use default values (techeyadmin333@gmail.com / techey333)
// php artisan app:create-admin-user

# Custom email and password
// php artisan app:create-admin-user --email=admin@example.com --password=mypassword123

# Custom username, email, and password
// php artisan app:create-admin-user --username=superadmin --email=admin@example.com --password=mypassword123
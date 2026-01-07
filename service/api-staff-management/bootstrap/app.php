<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Http\Request;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
        apiPrefix: 'api',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        // Register Spatie role/permission middleware aliases
        $middleware->alias([
            'role' => \Spatie\Permission\Middleware\RoleMiddleware::class,
            'permission' => \Spatie\Permission\Middleware\PermissionMiddleware::class,
            'role_or_permission' => \Spatie\Permission\Middleware\RoleOrPermissionMiddleware::class,
            'gateway.auth' => \App\Domain\v1\Auth\Middleware\AuthenticateGatewaySession::class,
        ]);

        // This is an API-only application behind a gateway.
        // When a user is unauthenticated, we DON'T want Laravel
        // to redirect to a non-existent "login" route.
        // Instead, always return a 401 JSON response.
        $middleware->redirectGuestsTo(function (Request $request) {
            return null; // returning null tells Laravel not to redirect to "login"
        });
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();

import { useState } from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { NavLink, useNavigate } from 'react-router-dom';

interface LoginProps {
  onLogin?: () => void;
}

export function LoginForm({
  className,
  onLogin,
  ...props
}: React.ComponentPropsWithoutRef<"div"> & { onLogin?: () => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Вход:', { email, password });
    if (onLogin) onLogin(); // Устанавливаем isAuthenticated
    navigate('/'); // Перенаправляем на главную страницу
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl text-green-700">Вход</CardTitle>
          <CardDescription className="text-green-600">
            Введите email и пароль для входа в аккаунт
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="email" className="text-green-600">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password" className="text-green-600">Пароль</Label>
                  <a
                    href="#"
                    className="ml-auto inline-block text-sm text-green-600 underline-offset-4 hover:underline"
                  >
                    Забыли пароль?
                  </a>
                </div>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full bg-green-600 hover:bg-green-700">
                Войти
              </Button>
              <Button variant="outline" className="w-full border-green-600 text-green-600 hover:bg-green-100">
                Войти через Google
              </Button>
            </div>
            <div className="mt-4 text-center text-sm text-green-600">
              Нет аккаунта?{' '}
              <NavLink to="/register" className="underline underline-offset-4 hover:text-green-700">
                Зарегистрируйтесь
              </NavLink>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-100 to-green-50 flex items-center justify-center p-6 md:p-10">
      <LoginForm onLogin={onLogin} />
    </div>
  );
};

export default Login;
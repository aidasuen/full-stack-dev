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
import { NavLink } from 'react-router-dom';

export function RegisterForm({
  className,
  ...props
}: React.ComponentPropsWithoutRef<"div">) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Регистрация:', { username, email, password });
    alert('Регистрация выполнена (имитация)');
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl text-green-700">Регистрация</CardTitle>
          <CardDescription className="text-green-600">
            Заполните поля ниже, чтобы создать аккаунт
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRegister}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="username" className="text-green-600">Имя пользователя</Label>
                <Input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Введите имя"
                  required
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="email" className="text-green-600">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="m@example.com"
                  required
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="password" className="text-green-600">Пароль</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Введите пароль"
                  required
                />
              </div>
              <Button type="submit" className="w-full bg-green-600 hover:bg-green-700">
                Зарегистрироваться
              </Button>
            </div>
            <div className="mt-4 text-center text-sm text-green-600">
              Уже есть аккаунт?{' '}
              <NavLink to="/login" className="underline underline-offset-4 hover:text-green-700">
                Войдите
              </NavLink>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

const Register: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-100 to-green-50 flex items-center justify-center p-6 md:p-10">
      <RegisterForm />
    </div>
  );
};

export default Register;
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { NavLink } from 'react-router-dom';
import { FaRoute, FaUsers, FaTrophy } from 'react-icons/fa'; 

const Home: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-100 to-green-50 p-6">
      <div className="text-center mb-12 animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-green-700 to-green-500 bg-clip-text text-transparent mb-4">
          Добро пожаловать в EcoVoyage!
        </h1>
        <p className="text-lg text-green-600 max-w-2xl mx-auto">
          Начните своё экологичное путешествие: планируйте маршруты, общайтесь с сообществом и зарабатывайте награды за экологичный образ жизни.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        <Card className="bg-green-50 border-green-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          <CardHeader className="flex items-center space-x-4">
            <FaRoute className="text-green-600 text-3xl" />
            <div>
              <CardTitle className="text-green-700">Маршруты</CardTitle>
              <CardDescription className="text-green-600">Планируйте экологичные поездки</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <NavLink to="/routes">
              <Button className="w-full bg-green-600 hover:bg-green-700 transition-transform duration-200 hover:scale-105">
                Перейти
              </Button>
            </NavLink>
          </CardContent>
        </Card>

        <Card className="bg-green-50 border-green-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          <CardHeader className="flex items-center space-x-4">
            <FaUsers className="text-green-600 text-3xl" />
            <div>
              <CardTitle className="text-green-700">Сообщество</CardTitle>
              <CardDescription className="text-green-600">Общайтесь с единомышленниками</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <NavLink to="/community">
              <Button className="w-full bg-green-600 hover:bg-green-700 transition-transform duration-200 hover:scale-105">
                Перейти
              </Button>
            </NavLink>
          </CardContent>
        </Card>

        <Card className="bg-green-50 border-green-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          <CardHeader className="flex items-center space-x-4">
            <FaTrophy className="text-green-600 text-3xl" />
            <div>
              <CardTitle className="text-green-700">Награды</CardTitle>
              <CardDescription className="text-green-600">Зарабатывайте достижения</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <NavLink to="/rewards">
              <Button className="w-full bg-green-600 hover:bg-green-700 transition-transform duration-200 hover:scale-105">
                Перейти
              </Button>
            </NavLink>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Home;
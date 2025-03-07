const Rewards: React.FC = () => {
  const rewards = [
    {
      title: "Эко-Новичок",
      description: "Начни с малого — пройди свой первый маршрут экологично.",
      condition: "1 эко-маршрут",
      color: "bg-green-500",
    },
    {
      title: "Зелёный Путешественник",
      description: "Стань мастером общественного транспорта.",
      condition: "5 поездок",
      color: "bg-green-600",
    },
    {
      title: "Чемпион Экологии",
      description: "Докажи, что ты настоящий защитник природы!",
      condition: "10 маршрутов",
      color: "bg-green-700",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-100 to-green-50 p-6">
      <div className="w-full max-w-5xl mx-auto">
        <h2 className="text-4xl font-bold text-green-800 mb-4 text-center">Награды за эко-жизнь</h2>
        <p className="text-lg text-green-600 mb-8 text-center">
          Получай награды за свои экологичные маршруты и вдохновляй других!
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {rewards.map((reward, index) => (
            <div
              key={index}
              className={`${reward.color} p-6 rounded-xl shadow-lg text-white hover:shadow-xl hover:scale-105 transition-all duration-300`}
            >
              <h3 className="text-2xl font-bold mb-3">{reward.title}</h3>
              <p className="text-white mb-3">{reward.description}</p>
              <p className="text-sm italic text-green-100">Условие: {reward.condition}</p>
            </div>
          ))}
        </div>
        <div className="mt-12 text-center">
          <p className="text-green-700 text-lg">
            Продолжай двигаться экологично, чтобы открыть новые достижения!
          </p>
        </div>
      </div>
    </div>
  );
};

export default Rewards;
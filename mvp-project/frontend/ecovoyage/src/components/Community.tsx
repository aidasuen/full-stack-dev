import { useState } from 'react';
import { cn } from '@/lib/utils'; 
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

const Community: React.FC = () => {
  const [posts, setPosts] = useState<string[]>([]);
  const [newPost, setNewPost] = useState('');

  const handlePost = () => {
    if (newPost.trim()) {
      setPosts([...posts, newPost]);
      setNewPost('');
    }
  };

  return (
    <div className="p-6 bg-gradient-to-b from-green-100 to-green-50 min-h-screen">
      <h1 className="text-3xl font-bold text-green-700 mb-6">Эко-сообщество</h1>
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-green-600">Напиши пост</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-4">
          <Input
            value={newPost}
            onChange={(e) => setNewPost(e.target.value)}
            placeholder="Поделись мыслями..."
            className="flex-1"
          />
          <Button
            onClick={handlePost}
            className={cn(
              'bg-green-600 hover:bg-green-700', 
              !newPost.trim() && 'opacity-50 cursor-not-allowed' 
            )}
            disabled={!newPost.trim()} 
          >
            Опубликовать
          </Button>
        </CardContent>
      </Card>
      <div className="space-y-4">
        {posts.map((post, index) => (
          <Card key={index} className="bg-green-50">
            <CardContent className="p-4 text-green-700">{post}</CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Community;
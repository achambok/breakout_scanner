import React from 'react';
import { Button } from '../components/ui/Button';

const HomePage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-gray-800">Welcome to Next.js with Shadcn and Tailwind CSS</h1>
      <p className="mt-4 text-lg text-gray-600">This is a sleek and modern application.</p>
      <Button onClick={() => alert('Button clicked!')} className="mt-6">
        Click Me
      </Button>
    </div>
  );
};

export default HomePage;
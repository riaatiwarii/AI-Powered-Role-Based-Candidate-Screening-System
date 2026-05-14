"""
Role selector component.
"""

'use client';

import { useState, useEffect } from 'react';
import { apiService } from '@/app/services/api';

interface RoleSelectorProps {
  selectedRole: string;
  onRoleChange: (role: string) => void;
}

const ROLE_DESCRIPTIONS: Record<string, string> = {
  backend_engineer: 'Building scalable server-side systems and APIs',
  ai_ml_engineer: 'Developing machine learning models and AI solutions',
  frontend_engineer: 'Creating responsive and interactive user interfaces',
  fullstack_engineer: 'Handling both frontend and backend development',
  data_engineer: 'Designing and managing data pipelines and warehouses',
};

export default function RoleSelector({ selectedRole, onRoleChange }: RoleSelectorProps) {
  const [roles, setRoles] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    try {
      const data = await apiService.getAvailableRoles();
      setRoles(data.roles);
      if (!selectedRole && data.roles.length > 0) {
        onRoleChange(data.roles[0]);
      }
    } catch (error) {
      console.error('Failed to fetch roles:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading roles...</div>;
  }

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4">👔 Select Your Target Role</h2>

      <div className="space-y-3">
        {roles.map((role) => (
          <label key={role} className="flex items-start p-3 border-2 rounded-lg cursor-pointer transition" style={{
            borderColor: selectedRole === role ? '#4f46e5' : '#e5e7eb',
            backgroundColor: selectedRole === role ? '#f0f4ff' : 'white',
          }}>
            <input
              type="radio"
              name="role"
              value={role}
              checked={selectedRole === role}
              onChange={(e) => onRoleChange(e.target.value)}
              className="mt-1 mr-3"
            />
            <div>
              <p className="font-semibold capitalize">{role.replace(/_/g, ' ')}</p>
              <p className="text-sm text-gray-600">{ROLE_DESCRIPTIONS[role]}</p>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}

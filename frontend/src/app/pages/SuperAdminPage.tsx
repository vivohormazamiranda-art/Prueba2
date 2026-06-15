// frontend/src/pages/SuperAdminPage.tsx
import { useState, useEffect } from "react";
import { getUsers, toggleUserStatus, changeUserRole, deleteUser } from "../services/api";
import { ApiUser } from "../services/api";

const ROLES = ["superadmin", "admin", "teacher", "student"];
export function SuperAdminPage() {
  const [users, setUsers] = useState<ApiUser[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await getUsers();
      setUsers(data);
    } catch {
      setError("Error al cargar usuarios");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (userId: string) => {
    try {
      await toggleUserStatus(userId);
      await loadUsers();
    } catch {
      setError("Error al cambiar estado");
    }
  };

  const handleChangeRole = async (userId: string, role: string) => {
    try {
      await changeUserRole(userId, role);
      await loadUsers();
    } catch {
      setError("Error al cambiar rol");
    }
  };

  const handleDelete = async (userId: string) => {
    if (!confirm("¿Eliminar usuario? Esta acción no se puede deshacer.")) return;
    try {
      await deleteUser(userId);
      await loadUsers();
    } catch {
      setError("Error al eliminar usuario");
    }
  };

  const filtered = users.filter(u =>
    u.name?.toLowerCase().includes(search.toLowerCase()) ||
    u.email?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Panel SuperAdmin — Gestión de Usuarios
        </h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
            <button onClick={() => setError(null)} className="ml-4 font-bold">✕</button>
          </div>
        )}

        <input
          type="text"
          placeholder="Buscar por nombre o email..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full p-3 border rounded-lg mb-6 shadow-sm"
        />

        {loading ? (
          <p>Cargando usuarios...</p>
        ) : (
          <div className="bg-white rounded-xl shadow overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-800 text-white">
                <tr>
                  <th className="p-3 text-left">Nombre</th>
                  <th className="p-3 text-left">Email</th>
                  <th className="p-3 text-left">Rol</th>
                  <th className="p-3 text-left">Estado</th>
                  <th className="p-3 text-left">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(user => (
                  <tr key={user.id} className="border-b hover:bg-gray-50">
                    <td className="p-3">{user.name}</td>
                    <td className="p-3">{user.email}</td>
                    <td className="p-3">
                      <select
                        value={user.role}
                        onChange={e => handleChangeRole(user.id, e.target.value)}
                        disabled={user.role === "SUPERADMIN"}
                        className="border rounded p-1 text-xs"
                      >
                        {ROLES.map(r => (
                          <option key={r} value={r}>{r}</option>
                        ))}
                      </select>
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        user.status === "active"
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}>
                        {user.status === "active" ? "Activo" : "Inactivo"}
                      </span>
                    </td>
                    <td className="p-3 flex gap-2">
                      <button
                        onClick={() => handleToggleStatus(user.id)}
                        className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded hover:bg-yellow-200"
                      >
                        {user.status === "active" ? "Desactivar" : "Activar"}
                      </button>
                      {user.role !== "SUPERADMIN" && (
                        <button
                          onClick={() => handleDelete(user.id)}
                          className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded hover:bg-red-200"
                        >
                          Eliminar
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
import React from "react";
import { Label } from "./../ui";

interface ProviderSelectProps {
  providers: string[];
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const ProviderSelect: React.FC<ProviderSelectProps> = ({ providers, value, onChange, disabled }) => {
  return (
      <div className="flex flex-col gap-1">
        <Label htmlFor="provider">Provider</Label>
      <select
        id="provider"
        name="provider"
        value={value}
        onChange={e => onChange(e.target.value)}
        disabled={disabled || providers.length === 0}
        className="border rounded px-2 py-1"
      >
        {providers.length === 0 ? (
          <option value="">Cargando providers...</option>
        ) : (
          providers.map(p => (
            <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
          ))
        )}
      </select>
    </div>
  );
};

export default ProviderSelect;

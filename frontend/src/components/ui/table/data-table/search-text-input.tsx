import { useEffect, useState } from "react";

import { Icons, Input } from "@/components";
import type { AvailableRoutesId } from "@/config/router";
import { useSearchText } from "@/hooks";
import { useTranslation } from "@/i18n";

type SearchTextInputProps = {
  path: AvailableRoutesId;
  placeholder?: string;
};

export const SearchTextInput = ({ path, placeholder }: SearchTextInputProps) => {
  const { t } = useTranslation();
  const {
    actions: { setPaginatedSearchText },
    searchText,
  } = useSearchText(path);

  const [localSearchValue, setLocalSearchValue] = useState(searchText ?? "");

  useEffect(() => {
    setLocalSearchValue(searchText ?? "");
  }, [searchText]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setLocalSearchValue(value);
    setPaginatedSearchText(value);
  };

  return (
    <Input
      className="max-w-sm"
      left={<Icons.Search />}
      onChange={handleSearchChange}
      placeholder={placeholder ?? t("common.filter")}
      value={localSearchValue}
    />
  );
};

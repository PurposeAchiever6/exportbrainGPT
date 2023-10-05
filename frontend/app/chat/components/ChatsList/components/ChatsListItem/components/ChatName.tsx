interface ChatNameProps {
  name: string;
  editing?: boolean;
  setName: (name: string) => void;
}

export const ChatName = ({
  setName,
  name,
  editing = false,
}: ChatNameProps): JSX.Element => {
  if (editing) {
    return (
      <input
        onChange={(event) => setName(event.target.value)}
        autoFocus
        value={name}
      />
    );
  }

  return <p>{name}</p>;
};

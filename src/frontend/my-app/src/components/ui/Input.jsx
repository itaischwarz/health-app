export function Input({
  id,
  type = "text",
  placeholder = "",
  className = "",
  ...props
}) {
  return (
    <input
      id={id}
      type={type}
      placeholder={placeholder}
      className={`w-full px-3 py-2 border border-gray-300 rounded-md ${className}`}
      {...props}
    />
  );
}

export function LoginPage() {
  return (
    <main>
      <form>
        <label htmlFor="account">帳號</label>
        <input id="account" name="account" type="text" />

        <label htmlFor="password">密碼</label>
        <input id="password" name="password" type="password" />

        <button type="submit">登入</button>
      </form>
    </main>
  );
}

import React, { useEffect, useState } from "react";
import styles from "./CompanyRecordsPage.module.css";
import { recordsService } from "../../services/recordsService.js";

const CompanyRecordsPage = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const data = await recordsService.getRecords();
        setRecords(data);
      } catch (err) {
        console.error(err);
        setError("Не удалось загрузить записи");
      } finally {
        setLoading(false);
      }
    };

    fetchRecords();
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className={styles.container}>
      <h2>Записи в компанию</h2>

      <table className={styles.table}>
        <thead>
        <tr>
          <th>ID</th>
          <th>Клиент</th>
          <th>Услуга</th>
          <th>Время</th>
        </tr>
        </thead>

        <tbody>
        {records.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.client}</td>
            <td>{item.service}</td>
            <td>{item.time}</td>
          </tr>
        ))}
        </tbody>
      </table>
    </div>
  );
};

export default CompanyRecordsPage;
